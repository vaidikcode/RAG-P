from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings

class VectorStoreManager:
    def __init__(self):
        self.vector_store = None
        self.document_count = 0

    def create_vector_store(self, documents: List[Document], embeddings: Embeddings):
        print("Creating vector store and indexing documents...")
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings
        )
        
        self.document_count = len(documents)
        print(f"Indexed {self.document_count} documents in vector store")
        
        return self.vector_store

    def get_vector_store(self):
        return self.vector_store

    def show_sources(self):
        if self.vector_store:
            print(f"Vector store contains {self.document_count} document chunks")
        else:
            print("Vector store not initialized")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.similarity_search(query, k=k)
