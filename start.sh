#!/bin/bash

echo "Starting RAG Application Services..."
echo "==================================="

# Function to kill background processes on exit
cleanup() {
    echo "Stopping all services..."
    kill $PYTHON_PID $GO_PID $REACT_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "1. Starting Python RAG service..."
cd RAG
python rag_service.py &
PYTHON_PID=$!
echo "Python RAG service started (PID: $PYTHON_PID)"

sleep 3

echo "2. Starting Go backend..."
cd ../RAG_backend
go run main.go &
GO_PID=$!
echo "Go backend started (PID: $GO_PID)"

sleep 3

echo "3. Starting React frontend..."
cd ../RAG_frontend
npm start &
REACT_PID=$!
echo "React frontend started (PID: $REACT_PID)"

echo ""
echo "All services started successfully!"
echo "- Python RAG Service: http://localhost:8080"
echo "- Go Backend: http://localhost:8090"
echo "- React Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

wait
