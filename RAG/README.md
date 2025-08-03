# RAG Application with DeepSeek R1

A clean, modular RAG (Retrieval-Augmented Generation) application using LangChain and DeepSeek R1 8B model via Ollama.

## Setup

1. Install Ollama and pull the DeepSeek model:
```bash
ollama pull deepseek-r1:8b
ollama serve
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

## Usage

- Ask questions about the loaded documents
- Type 'sources' to see available documents
- Type 'quit' to exit

## Architecture

- `app.py` - Main application entry point
- `document_manager.py` - Document loading and processing
- `vector_store.py` - Vector store management
- `llm_manager.py` - LLM and embeddings management
- `rag_chain.py` - RAG chain implementation
- `main.py` - Alternative single-file implementation
