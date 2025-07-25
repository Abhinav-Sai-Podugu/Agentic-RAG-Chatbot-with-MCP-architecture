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

## 📡 MCP Message Flow

```bash
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "RETRIEVAL_RESULT",
  "trace_id": "abc-123-def",
  "timestamp": "2024-01-20T10:30:00Z",
  "payload": {
    "retrieved_context": ["relevant chunk 1", "relevant chunk 2"],
    "context_metadata": [{"source_file": "doc.pdf", "chunk_id": "doc_chunk_1"}],
    "query": "What are the key metrics?"
  }
}
```

## 📁 Project Structure

```bash
agentic_rag_chatbot/
│
├── agents/
│   ├── __init__.py
│   ├── coordinator.py          # MCP message orchestration
│   ├── ingestion_agent.py      # Document parsing agent
│   ├── retrieval_agent.py      # Vector storage & retrieval
│   └── llm_response_agent.py   # Response generation
│
├── mcp/
│   ├── __init__.py
│   └── message.py              # MCP message utilities
│
├── vectorstore/
│   ├── __init__.py
│   └── store.py                # Vector database implementation
│
├── ui/
│   ├── __init__.py
│   └── app.py                  # Streamlit frontend
│
├── utils/
│   ├── __init__.py
│   └── parser_utils.py         # Document parsers
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration settings
│
├── requirements.txt
├── README.md
├── .env.example
└── run.py                      # Application entry point
```

## 🚀 Quick Setup

1. Clone Repository
   
```bash
git clone https://github.com/yourusername/agentic-rag-chatbot.git
cd agentic-rag-chatbot
```

2. Install Dependencies
   
```bash
pip install -r requirements.txt
```

3. Environment Setup

   Create a .env file:
   
```bash
# Copy example environment file
cp .env.example .env

# Edit with your API key
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

4. Run Application

```bash
# Using run.py
python run.py

# Or directly with Streamlit
streamlit run ui/app.py
```

5. Access Application

Open your browser and navigate to: http://localhost:8501

📋 Requirements

```bash
streamlit>=1.28.0
sentence-transformers>=2.2.2
scikit-learn>=1.3.0
PyPDF2>=3.0.1
python-docx>=0.8.11
python-pptx>=0.6.21
requests>=2.31.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

🔧 Configuration

Environment Variables

Create a .env file with:

```bash
# Required: OpenRouter API Key for LLM access
OPENROUTER_API_KEY=your_api_key_here

# Optional: Model Configuration
LLM_MODEL=mistralai/mistral-7b-instruct
EMBEDDING_MODEL=all-MiniLM-L6-v2
MAX_CHUNKS_RETRIEVAL=5
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

Supported LLM Models

The system uses OpenRouter API and supports:

- mistralai/mistral-7b-instruct (default)

- anthropic/claude-instant-v1

- And many more available through OpenRouter (Preffered: Use lighter models)
