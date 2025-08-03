#!/bin/bash

echo "RAG Application Setup Script"
echo "============================="

echo "Setting up MySQL database..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS rag_db;"
echo "Database created successfully!"

echo ""
echo "Setting up Python RAG service..."
cd RAG
python -m pip install -r flask_requirements.txt
echo "Python dependencies installed!"

echo ""
echo "Setting up Go backend..."
cd ../RAG_backend
go mod tidy
go mod download
echo "Go dependencies installed!"

echo ""
echo "Setting up React frontend..."
cd ../RAG_frontend
npm install
echo "React dependencies installed!"

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start Ollama: ollama serve"
echo "2. Start Python RAG service: cd RAG && python rag_service.py"
echo "3. Start Go backend: cd RAG_backend && go run main.go"
echo "4. Start Frontend: cd RAG_frontend && npm start"
