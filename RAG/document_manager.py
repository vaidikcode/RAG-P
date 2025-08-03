import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4

class DocumentManager:
    def __init__(self, documents_path: str = "documents"):
        self.documents_path = documents_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Optimized for better precision
            chunk_overlap=100,  # Better context continuity
            separators=["\n\n", "\n", ". ", " "],  # Better splitting points
            add_start_index=True
        )

    def load_documents(self) -> List[Document]:
        docs = []
        
        if os.path.exists(self.documents_path) and os.listdir(self.documents_path):
            try:
                loader = DirectoryLoader(
                    self.documents_path, 
                    glob="*.txt", 
                    loader_cls=TextLoader
                )
                file_docs = loader.load()
                if file_docs:
                    docs.extend(file_docs)
                    print(f"Loaded {len(file_docs)} local documents")
            except Exception as e:
                print(f"Error loading local documents: {e}")
        
        if not docs:
            try:
                loader = WebBaseLoader(
                    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
                    bs_kwargs=dict(
                        parse_only=bs4.SoupStrainer(
                            class_=("post-content", "post-title", "post-header")
                        )
                    )
                )
                docs = loader.load()
                print(f"Loaded {len(docs)} web documents")
            except Exception as e:
                print(f"Could not load web documents: {e}")
                docs = self._get_fallback_documents()
        
        return docs

    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks")
        return chunks

    def _get_fallback_documents(self) -> List[Document]:
        return [
            Document(
                page_content="Retrieval-Augmented Generation (RAG) combines retrieval and generation to provide more accurate responses by accessing external knowledge sources.",
                metadata={"source": "rag_intro"}
            ),
            Document(
                page_content="LangChain provides tools for building AI applications with document loading, embeddings, vector stores, and chain orchestration capabilities.",
                metadata={"source": "langchain_intro"}
            ),
            Document(
                page_content="DeepSeek R1 is a powerful language model that excels at reasoning and can be run locally using Ollama for privacy and control.",
                metadata={"source": "deepseek_intro"}
            )
        ]
