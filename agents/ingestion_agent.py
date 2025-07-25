from utils.parser_utils import parse_document
from mcp.message import create_mcp_message
import logging

logger = logging.getLogger(__name__)


class IngestionAgent:
    def process(self, file_paths, trace_id=None):
        """
        Parse documents and return MCP message with chunks
        """
        try:
            parsed_docs = []
            file_metadata = []

            for file_path in file_paths:
                logger.info(f"Processing file: {file_path}")
                chunks = parse_document(file_path)

                # Add metadata for each chunk
                for i, chunk in enumerate(chunks):
                    parsed_docs.append({
                        "content": chunk,
                        "source_file": file_path.split('/')[-1],  # Just filename
                        "chunk_id": f"{file_path.split('/')[-1]}_chunk_{i}",
                        "chunk_index": i
                    })

                file_metadata.append({
                    "filename": file_path.split('/')[-1],
                    "chunks_count": len(chunks),
                    "file_type": file_path.split('.')[-1].lower()
                })

            return create_mcp_message(
                sender="IngestionAgent",
                receiver="RetrievalAgent",
                msg_type="DOC_PARSED",
                payload={
                    "chunks": parsed_docs,
                    "total_chunks": len(parsed_docs),
                    "files_processed": file_metadata
                },
                trace_id=trace_id
            )

        except Exception as e:
            logger.error(f"Error in IngestionAgent: {str(e)}")
            return create_mcp_message(
                sender="IngestionAgent",
                receiver="RetrievalAgent",
                msg_type="DOC_PARSE_ERROR",
                payload={
                    "error": str(e),
                    "files_attempted": [f.split('/')[-1] for f in file_paths]
                },
                trace_id=trace_id
            )