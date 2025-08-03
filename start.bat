@echo off
echo Starting RAG Application Services...
echo =======================================

echo 1. Starting Python RAG service...
start "Python RAG Service" cmd /k "cd RAG && python rag_service.py"
timeout /t 3 /nobreak > nul

echo 2. Starting Go backend...
start "Go Backend" cmd /k "cd RAG_backend && go run main.go"
timeout /t 3 /nobreak > nul

echo 3. Starting React frontend...
start "React Frontend" cmd /k "cd RAG_frontend && npm start"

echo.
echo All services are starting in separate windows!
echo - Python RAG Service: http://localhost:8080
echo - Go Backend: http://localhost:8090
echo - React Frontend: http://localhost:3000
echo.
echo Close individual command windows to stop services.

pause
