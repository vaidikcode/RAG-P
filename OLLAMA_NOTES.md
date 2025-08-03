# Ollama Configuration to reduce warnings
# Add these to your Python RAG service

OLLAMA_OPTIONS='{
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "repeat_penalty": 1.1
}'

# Note: These warnings are harmless and can be ignored
# The model works perfectly without these advanced parameters
