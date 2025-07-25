from mcp.message import create_mcp_message
import os
import requests
import json
import logging
from config.settings import OPENROUTER_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)


class LLMResponseAgent:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.chat_history = []

    def process(self, retrieval_message):
        """
        Generate final response using retrieved context
        Returns MCP message with final answer
        """
        try:
            if retrieval_message["type"] == "RETRIEVAL_ERROR":
                return create_mcp_message(
                    sender="LLMResponseAgent",
                    receiver="Coordinator",
                    msg_type="LLM_ERROR",
                    payload={
                        "error": "Cannot generate response due to retrieval error",
                        "retrieval_error": retrieval_message["payload"]["error"]
                    },
                    trace_id=retrieval_message["trace_id"]
                )

            # Extract context and query
            context_chunks = retrieval_message["payload"]["retrieved_context"]
            context_metadata = retrieval_message["payload"]["context_metadata"]
            question = retrieval_message["payload"]["query"]

            # Build context with source information
            formatted_context = ""
            for i, (chunk, metadata) in enumerate(zip(context_chunks, context_metadata)):
                formatted_context += f"[Source: {metadata['source_file']}]\n{chunk}\n\n"

            # Create the prompt
            system_prompt = """You are a knowledgeable assistant that answers questions based on provided context. 
            Always cite the source files when referencing information. Be accurate and concise."""

            user_prompt = f"""Context from uploaded documents:
{formatted_context}

Question: {question}

Please provide a comprehensive answer based on the context above. If the context doesn't contain enough information to fully answer the question, please say so."""

            # Add to chat history
            self.chat_history.append({"role": "user", "content": user_prompt})

            # Make API call
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    *self.chat_history
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

            answer = response_data["choices"][0]["message"]["content"]

            # Add assistant response to history
            self.chat_history.append({"role": "assistant", "content": answer})

            logger.info(f"Generated LLM response for query: {question[:50]}...")

            return create_mcp_message(
                sender="LLMResponseAgent",
                receiver="Coordinator",
                msg_type="LLM_RESPONSE",
                payload={
                    "answer": answer,
                    "sources": context_chunks,
                    "source_metadata": context_metadata,
                    "query": question,
                    "model_used": "mistralai/mistral-7b-instruct",
                    "context_chunks_used": len(context_chunks)
                },
                trace_id=retrieval_message["trace_id"]
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return create_mcp_message(
                sender="LLMResponseAgent",
                receiver="Coordinator",
                msg_type="LLM_ERROR",
                payload={
                    "error": f"API request failed: {str(e)}",
                    "query": retrieval_message["payload"].get("query", "unknown")
                },
                trace_id=retrieval_message["trace_id"]
            )

        except Exception as e:
            logger.error(f"Error in LLMResponseAgent: {str(e)}")
            return create_mcp_message(
                sender="LLMResponseAgent",
                receiver="Coordinator",
                msg_type="LLM_ERROR",
                payload={
                    "error": str(e),
                    "query": retrieval_message["payload"].get("query", "unknown")
                },
                trace_id=retrieval_message["trace_id"]
            )