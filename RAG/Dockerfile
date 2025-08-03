FROM python:3.11-slim

WORKDIR /app

COPY flask_requirements.txt .
RUN pip install -r flask_requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "rag_service.py"]
