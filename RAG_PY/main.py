import os
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

def main():
    # Initialize Ollama with DeepSeek model (same as Go version)
    llm = Ollama(
        model="deepseek-r1:8b",
        base_url="http://127.0.0.1:11434"  # Same Ollama server
    )
    
    # Create conversation memory (equivalent to Go's ConversationBuffer)
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )
    
    print("Chat Application Started! Type 'quit' to exit.")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() == "quit":
            break
            
        try:
            # Get response from LLM
            response = llm.invoke(user_input)
            print(f"AI: {response}\n")
            
            # Store conversation in memory
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(response)
            
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
