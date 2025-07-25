from mcp.message import create_mcp_message
import logging

logger = logging.getLogger(__name__)


class RetrievalAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.stored_chunks = []  # Keep track of stored chunks with metadata

    def process(self, ingestion_message):
        """
        Store document chunks in vector database
        Returns MCP message confirming storage
        """
        try:
            if ingestion_message["type"] == "DOC_PARSE_ERROR":
                return create_mcp_message(
                    sender="RetrievalAgent",
                    receiver="Coordinator",
                    msg_type="STORAGE_ERROR",
                    payload={"error": "Cannot store documents due to parsing error"},
                    trace_id=ingestion_message["trace_id"]
                )

            chunks_data = ingestion_message["payload"]["chunks"]

            # Extract just the text content for vector store
            chunk_texts = [chunk["content"] for chunk in chunks_data]

            # Store in vector database
            self.vector_store.add_documents(chunk_texts)

            # Keep metadata for retrieval context
            self.stored_chunks = chunks_data

            logger.info(f"Stored {len(chunk_texts)} chunks in vector database")

            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="Coordinator",
                msg_type="STORAGE_COMPLETE",
                payload={
                    "chunks_stored": len(chunk_texts),
                    "files_processed": ingestion_message["payload"]["files_processed"]
                },
                trace_id=ingestion_message["trace_id"]
            )

        except Exception as e:
            logger.error(f"Error storing documents: {str(e)}")
            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="Coordinator",
                msg_type="STORAGE_ERROR",
                payload={"error": str(e)},
                trace_id=ingestion_message["trace_id"]
            )

    def retrieve(self, query, trace_id=None, top_k=5):
        """
        Retrieve relevant chunks for query
        Returns MCP message with retrieved context
        """
        try:
            # Get similar chunks from vector store
            similar_chunks = self.vector_store.query(query, top_k=top_k)

            # Find metadata for retrieved chunks
            retrieved_context = []
            chunk_metadata = []

            for chunk_text in similar_chunks:
                # Find corresponding metadata
                for stored_chunk in self.stored_chunks:
                    if stored_chunk["content"] == chunk_text:
                        retrieved_context.append(chunk_text)
                        chunk_metadata.append({
                            "source_file": stored_chunk["source_file"],
                            "chunk_id": stored_chunk["chunk_id"],
                            "chunk_index": stored_chunk["chunk_index"]
                        })
                        break

            logger.info(f"Retrieved {len(retrieved_context)} relevant chunks for query: {query[:50]}...")

            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                msg_type="RETRIEVAL_RESULT",
                payload={
                    "retrieved_context": retrieved_context,
                    "context_metadata": chunk_metadata,
                    "query": query,
                    "similarity_scores": "cosine_similarity_used"  # Could add actual scores
                },
                trace_id=trace_id
            )

        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return create_mcp_message(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                msg_type="RETRIEVAL_ERROR",
                payload={
                    "error": str(e),
                    "query": query
                },
                trace_id=trace_id
            )