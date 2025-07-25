# 🤖 Agentic RAG Chatbot

An intelligent document Q&A system built with Agent-Based Architecture and Model Context Protocol (MCP) for seamless multi-format document processing and retrieval-augmented generation.


## 🌟 Features

### 📚 Multi-Format Document Support

✅ PDF - Extracts text from all pages

✅ DOCX - Processes Word documents

✅ PPTX - Handles PowerPoint presentations

✅ CSV - Intelligent row grouping and header processing

✅ TXT/Markdown - Smart paragraph and section-based chunking


## 🏗️ Agentic Architecture

Three specialized agents communicate via Model Context Protocol (MCP):

📝 IngestionAgent - Parses and preprocesses documents

🔍 RetrievalAgent - Handles embeddings and semantic search

🤖 LLMResponseAgent - Generates contextual responses


## 🔄 Model Context Protocol (MCP)

Structured message passing between agents

Complete traceability with unique trace IDs

Error handling and status tracking

Real-time message flow visualization


## 🎯 Advanced Features

Vector Store Integration - Semantic similarity search

Multi-turn Conversations - Maintains chat history

Source Attribution - Shows which document chunks were used

Real-time Processing - Live agent communication tracking

Responsive UI - Modern chat interface with Streamlit


## 🏗️ Architecture

```bash
graph TD
    A[User Upload Documents] --> B[UI Layer - Streamlit]
    B --> C[Coordinator]
    C --> D[IngestionAgent]
    C --> E[RetrievalAgent] 
    C --> F[LLMResponseAgent]
    
    D -->|MCP Message| E
    E -->|MCP Message| F
    F -->|MCP Message| C
    
    E --> G[Vector Store]
    F --> H[OpenRouter API]
    
    subgraph "MCP Messages"
        I[DOC_PARSED]
        J[STORAGE_COMPLETE]
        K[RETRIEVAL_RESULT]
        L[LLM_RESPONSE]
    end
```
