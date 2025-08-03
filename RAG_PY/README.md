# RAG Python Chatbot

Python implementation of the chatbot using LangChain and Ollama, equivalent to the Go version.

## Features

- ✅ Same DeepSeek R1 8B model as Go version
- ✅ Conversation memory
- ✅ Local inference via Ollama
- ✅ Simple chat interface
- ✅ Error handling
- ✅ Same configuration as Go version

## Quick Setup

1. **Navigate to the Python folder:**
   ```bash
   cd RAG_PY
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Or install manually:**
   ```bash
   pip install -r requirements.txt
   ```

## Prerequisites

1. **Ollama server must be running:**
   ```bash
   ollama serve
   ```

2. **DeepSeek R1 8B model must be available:**
   ```bash
   ollama pull deepseek-r1:8b
   ```

## Usage

```bash
python main.py
```

## Example Session

```
Chat Application Started! Type 'quit' to exit.
You: Hello, how are you?
AI: Hello! I'm doing well, thank you for asking. I'm here and ready to help you with any questions or tasks you might have. How are you doing today?

You: Explain quantum computing
AI: Quantum computing is a revolutionary approach to computation that harnesses the principles of quantum mechanics...

You: quit
```

## Configuration

The Python version uses the same configuration as the Go version:

- **Model**: `deepseek-r1:8b`
- **Server**: `http://127.0.0.1:11434`
- **Memory**: Conversation buffer for chat history
- **Interface**: Command-line chat interface

## Dependencies

- `langchain` - Main LangChain library
- `langchain-community` - Community integrations (Ollama)
- `langchain-core` - Core LangChain components  
- `requests` - HTTP requests for setup script

## Troubleshooting

### Connection Refused Error
- Make sure Ollama server is running: `ollama serve`
- Check if running in WSL - use Windows PowerShell instead

### Model Not Found Error
- Pull the model: `ollama pull deepseek-r1:8b`
- Check available models: `ollama list`

### Import Errors
- Install dependencies: `pip install -r requirements.txt`
- Use Python 3.8+ 

## Comparison with Go Version

| Feature | Go Version | Python Version |
|---------|------------|----------------|
| Model | `deepseek-r1:8b` | `deepseek-r1:8b` |
| Server | `127.0.0.1:11434` | `127.0.0.1:11434` |
| Memory | `memory.NewConversationBuffer()` | `ConversationBufferMemory()` |
| Interface | Same chat loop | Same chat loop |
| Error Handling | ✅ | ✅ |

Both versions provide identical functionality with their respective language ecosystems.
