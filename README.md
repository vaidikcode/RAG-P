# RAG Application - Full Stack

A complete RAG (Retrieval-Augmented Generation) application with React TypeScript frontend, Go backend with Gin and GORM, MySQL database, and Python RAG service using LangChain and DeepSeek R1 8B model.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │───▶│   Go Backend    │───▶│ Python RAG      │───▶│     Ollama      │
│   (Port 3000)   │    │   (Port 8090)   │    │ Service (8080)  │    │  DeepSeek R1    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ MySQL Database  │
                       │   (Port 3306)   │
                       └─────────────────┘
```

## Features

- 📄 **Document Upload**: Support for PDF and TXT files
- 🔍 **Intelligent Search**: RAG-powered question answering
- 💬 **Chat Interface**: Interactive conversation with your documents
- 📚 **Document Management**: View, delete, and organize uploaded documents
- 🎨 **Professional UI**: Clean, responsive design with Tailwind CSS
- 🔗 **Full Integration**: Seamless communication between all services

## Prerequisites

1. **MySQL Server** - Local MySQL installation
2. **Go** - Version 1.21 or later
3. **Node.js** - Version 16 or later
4. **Python** - Version 3.8 or later
5. **Ollama** - For running DeepSeek R1 8B model

## Quick Setup

### 1. Install Ollama and DeepSeek Model
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull DeepSeek R1 8B model
ollama pull deepseek-r1:8b

# Start Ollama service
ollama serve
```

### 2. Setup MySQL Database
```sql
CREATE DATABASE rag_db;
CREATE USER 'rag_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON rag_db.* TO 'rag_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Run Setup Script
```bash
# For Linux/Mac
chmod +x setup.sh
./setup.sh

# For Windows
setup.bat
```

## Manual Setup

### Backend (Go + GORM + MySQL)
```bash
cd RAG_backend
go mod tidy
go run main.go
```

### Python RAG Service
```bash
cd RAG
pip install -r flask_requirements.txt
python rag_service.py
```

### Frontend (React + TypeScript)
```bash
cd RAG_frontend
npm install
npm start
```

## Configuration

### Database Configuration
Update `RAG_backend/main.go`:
```go
dsn := "username:password@tcp(localhost:3306)/rag_db?charset=utf8mb4&parseTime=True&loc=Local"
```

### Ollama Configuration
Update model settings in `RAG/rag_service.py`:
```python
self.llm = Ollama(model="deepseek-r1:8b", base_url="http://127.0.0.1:11434")
```

## API Endpoints

### Document Management
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - Get all documents
- `DELETE /api/documents/:id` - Delete document

### Chat/RAG
- `POST /api/chat/query` - Process RAG query
- `GET /api/chat/history` - Get chat history

### Health Checks
- `GET /health` - Backend health
- `GET /rag/health` - Python service health

## Usage

1. **Start all services** in the correct order:
   - Ollama service
   - Python RAG service (port 8080)
   - Go backend (port 8090)
   - React frontend (port 3000)

2. **Upload documents** via the web interface

3. **Ask questions** about your uploaded documents

4. **View conversation history** and manage documents

## Project Structure

```
RAG-P/
├── RAG/                          # Python RAG service
│   ├── rag_service.py           # Flask RAG API
│   └── flask_requirements.txt   # Python dependencies
├── RAG_backend/                 # Go backend
│   ├── main.go                  # Server entry point
│   ├── database/                # Database connection
│   ├── handlers/                # HTTP handlers
│   ├── models/                  # Database models
│   └── services/                # Business logic
├── RAG_frontend/                # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── api.ts              # API client
│   │   └── types.ts            # TypeScript types
│   └── package.json
└── README.md
```

## Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Axios
- **Backend**: Go, Gin, GORM
- **Database**: MySQL
- **RAG Service**: Python, Flask, LangChain, ChromaDB
- **AI Model**: DeepSeek R1 8B via Ollama
- **File Processing**: PDF parsing, text extraction

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check model is available: `ollama list`

2. **Database Connection Failed**
   - Verify MySQL is running
   - Check database credentials
   - Ensure database exists

3. **Python Dependencies Issues**
   - Use virtual environment
   - Install with: `pip install -r flask_requirements.txt`

4. **Frontend API Errors**
   - Check backend is running on port 8090
   - Verify CORS configuration

## Development

### Adding New Document Types
1. Update `document_service.go` with new extraction logic
2. Add file type validation in frontend
3. Test with sample files

### Customizing RAG Behavior
1. Modify prompt template in `rag_service.py`
2. Adjust chunk size and overlap parameters
3. Change similarity search parameters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test all services
5. Submit a pull request

## License

This project is licensed under the MIT License.
