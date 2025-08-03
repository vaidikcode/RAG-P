"""
Setup script for RAG Python chatbot
Run this to install dependencies and test the setup
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_ollama_connection():
    """Test if Ollama server is running"""
    print("🔍 Testing Ollama connection...")
    try:
        import requests
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running!")
            
            # Check if deepseek model is available
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            if any('deepseek-r1:8b' in model for model in models):
                print("✅ DeepSeek R1 8B model is available!")
            else:
                print("⚠️  DeepSeek R1 8B model not found. Run: ollama pull deepseek-r1:8b")
            return True
        else:
            print("❌ Ollama server responded with error")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama server: {e}")
        print("Make sure to run 'ollama serve' in another terminal")
        return False

def main():
    print("🚀 Setting up RAG Python chatbot...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Make sure you're in the RAG_PY directory")
        return
    
    success = True
    
    # Install dependencies
    if not install_requirements():
        success = False
    
    print()
    
    # Test Ollama connection
    if not test_ollama_connection():
        success = False
    
    print("=" * 50)
    
    if success:
        print("🎉 Setup complete! Run 'python main.py' to start the chatbot")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print("\nQuick troubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Pull the model: ollama pull deepseek-r1:8b")
        print("3. Install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
