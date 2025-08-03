from document_manager import DocumentManager
from vector_store import VectorStoreManager  
from llm_manager import LLMManager
from rag_chain import RAGChain

class RAGApplication:
    def __init__(self):
        self.doc_manager = DocumentManager()
        self.vector_manager = VectorStoreManager()
        self.llm_manager = LLMManager()
        self.rag_chain = None
        self.setup_complete = False

    def setup(self):
        print("Initializing RAG Application...")
        
        llm = self.llm_manager.get_llm()
        embeddings = self.llm_manager.get_embeddings()
        
        documents = self.doc_manager.load_documents()
        chunks = self.doc_manager.split_documents(documents)
        
        vector_store = self.vector_manager.create_vector_store(chunks, embeddings)
        
        self.rag_chain = RAGChain(llm, vector_store)
        self.setup_complete = True
        
        print(f"RAG setup complete! Loaded {len(chunks)} document chunks.")

    def chat(self):
        if not self.setup_complete:
            self.setup()
        
        print("\nRAG Chat Application")
        print("Type 'quit' to exit, 'sources' to see loaded documents")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
                
            if user_input.lower() == "sources":
                self.vector_manager.show_sources()
                continue
                
            if not user_input:
                continue
            
            try:
                response = self.rag_chain.invoke(user_input)
                print(f"AI: {response['answer']}")
                
                if response.get('source_documents'):
                    print("\nSources:")
                    for i, doc in enumerate(response['source_documents'][:2], 1):
                        source = doc.metadata.get('source', 'Unknown')
                        preview = doc.page_content[:80] + "..."
                        print(f"  {i}. {source}: {preview}")
                        
            except Exception as e:
                print(f"Error: {e}")

def main():
    app = RAGApplication()
    try:
        app.chat()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()
