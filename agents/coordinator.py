from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from vectorstore.store import SimpleVectorStore
from mcp.message import create_mcp_message
from uuid import uuid4
import logging

# Setup logging for MCP message tracing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPCoordinator:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
        self.ingestion_agent = IngestionAgent()
        self.retrieval_agent = RetrievalAgent(self.vector_store)
        self.llm_agent = LLMResponseAgent()
        self.message_history = []  # Track all MCP messages for debugging

    def log_message(self, message):
        """Log MCP message for tracing"""
        logger.info(
            f"MCP Message: {message['sender']} -> {message['receiver']} | Type: {message['type']} | Trace: {message['trace_id']}")
        self.message_history.append(message)

    def run_pipeline(self, file_paths, query):
        # Generate single trace_id for the entire pipeline
        trace_id = str(uuid4())

        # Step 1: Ingestion Agent processes documents
        logger.info(f"Starting pipeline with trace_id: {trace_id}")

        ingestion_msg = self.ingestion_agent.process(file_paths, trace_id)
        self.log_message(ingestion_msg)

        # Step 2: Retrieval Agent stores documents
        storage_response = self.retrieval_agent.process(ingestion_msg)
        self.log_message(storage_response)

        # Step 3: Retrieval Agent retrieves relevant chunks
        retrieval_msg = self.retrieval_agent.retrieve(query, trace_id)
        self.log_message(retrieval_msg)

        # Step 4: LLM Agent generates final response
        llm_response_msg = self.llm_agent.process(retrieval_msg)
        self.log_message(llm_response_msg)

        # Return final response in the expected format for UI
        return {
            "answer": llm_response_msg["payload"]["answer"],
            "sources": llm_response_msg["payload"]["sources"],
            "trace_id": trace_id,
            "message_history": self.message_history[-4:]  # Last 4 messages for this pipeline
        }


# Create global coordinator instance
coordinator = MCPCoordinator()


def run_pipeline(file_paths, query):
    """Legacy function for backward compatibility"""
    return coordinator.run_pipeline(file_paths, query)