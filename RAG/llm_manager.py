from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

class LLMManager:
    def __init__(self, model_name: str = "deepseek-r1:8b", base_url: str = "http://127.0.0.1:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        self.embeddings = None

    def get_llm(self):
        if not self.llm:
            self.llm = Ollama(
                model=self.model_name,
                base_url=self.base_url
            )
            print(f"Initialized LLM: {self.model_name}")
        return self.llm

    def get_embeddings(self):
        if not self.embeddings:
            self.embeddings = OllamaEmbeddings(
                model=self.model_name,
                base_url=self.base_url
            )
            print(f"Initialized embeddings: {self.model_name}")
        return self.embeddings

    def test_connection(self):
        try:
            llm = self.get_llm()
            response = llm.invoke("Hello")
            print("LLM connection successful")
            return True
        except Exception as e:
            print(f"LLM connection failed: {e}")
            return False
