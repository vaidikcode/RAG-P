import os
import bs4
from typing import List
from typing_extensions import TypedDict

from langchain import hub
from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader, TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def setup_rag_pipeline():
    print("Setting up RAG pipeline...")
    
    llm = Ollama(model="deepseek-r1:8b", base_url="http://127.0.0.1:11434")
    embeddings = OllamaEmbeddings(model="deepseek-r1:8b", base_url="http://127.0.0.1:11434")
    
    print("Loading documents...")
    docs = []
    
    documents_folder = "documents"
    if os.path.exists(documents_folder) and os.listdir(documents_folder):
        try:
            txt_loader = DirectoryLoader(documents_folder, glob="*.txt", loader_cls=TextLoader)
            file_docs = txt_loader.load()
            if file_docs:
                docs.extend(file_docs)
                print(f"Loaded {len(file_docs)} text files")
        except Exception as e:
            print(f"Error loading local documents: {e}")
    
    if not docs:
        try:
            loader = WebBaseLoader(
                web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
                bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("post-content", "post-title", "post-header")))
            )
            docs = loader.load()
            print(f"Loaded {len(docs)} web documents")
        except Exception as e:
            print(f"Could not load web documents: {e}")
    
    if not docs:
        docs = [
            Document(
                page_content="Retrieval-Augmented Generation (RAG) combines retrieval and generation. It retrieves relevant documents from a knowledge base and uses them to generate better responses. RAG applications have two main components: indexing and retrieval-generation.",
                metadata={"source": "rag_info"}
            ),
            Document(
                page_content="LangChain is a framework for developing applications powered by language models. It provides tools for document loading, text splitting, embeddings, vector stores, and chains. LangGraph orchestrates complex RAG workflows.",
                metadata={"source": "langchain_info"}
            ),
            Document(
                page_content="DeepSeek R1 is a powerful language model that can be run locally using Ollama. It provides excellent performance for text generation, question answering, and reasoning tasks. The model supports context windows and can be fine-tuned for specific domains.",
                metadata={"source": "deepseek_info"}
            )
        ]
        print("Using sample documents")
    
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Optimized chunk size
        chunk_overlap=100,  # Better overlap
        separators=["\n\n", "\n", ". ", " "],  # Better splitting
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Created {len(all_splits)} document chunks")
    
    print("Creating vector store...")
    vector_store = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    print(f"Indexed {len(all_splits)} documents in vector store")
    
    try:
        prompt = hub.pull("rlm/rag-prompt")
        print("Loaded RAG prompt from hub")
    except Exception as e:
        from langchain_core.prompts import PromptTemplate
        template = """Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer:"""
        prompt = PromptTemplate.from_template(template)
        print("Using fallback prompt")
    
    return llm, vector_store, prompt

def retrieve(state: State, vector_store):
    retrieved_docs = vector_store.similarity_search(state["question"], k=4)
    return {"context": retrieved_docs}

def generate(state: State, llm, prompt):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    
    if hasattr(prompt, 'invoke'):
        try:
            messages = prompt.invoke({"question": state["question"], "context": docs_content})
            if hasattr(messages, 'to_messages'):
                formatted_prompt = messages.to_messages()[0].content
            else:
                formatted_prompt = str(messages)
        except:
            formatted_prompt = prompt.format(question=state["question"], context=docs_content)
    else:
        formatted_prompt = prompt.format(question=state["question"], context=docs_content)
    
    response = llm.invoke(formatted_prompt)
    return {"answer": response}

def main():
    print("RAG Chat Application with DeepSeek R1 8B")
    print("=" * 50)
    
    try:
        llm, vector_store, prompt = setup_rag_pipeline()
        
        print("\nRAG setup complete! Ask questions about the loaded documents.")
        print("Type 'quit' to exit, 'sources' to see available documents.")
        print("=" * 50)
        
        def retrieve_with_store(state: State):
            return retrieve(state, vector_store)
        
        def generate_with_llm(state: State):
            return generate(state, llm, prompt)
        
        graph_builder = StateGraph(State).add_sequence([retrieve_with_store, generate_with_llm])
        graph_builder.add_edge(START, "retrieve_with_store")
        graph = graph_builder.compile()
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "sources":
                print(f"Vector store contains {vector_store._collection.count()} document chunks")
                continue
                
            if not user_input:
                continue
            
            try:
                print("Searching documents and generating response...")
                result = graph.invoke({"question": user_input})
                print(f"AI: {result['answer']}")
                
                if result.get('context'):
                    print("\nRelevant sources:")
                    for i, doc in enumerate(result['context'][:3], 1):
                        source = doc.metadata.get('source', 'Unknown')
                        preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                        print(f"  {i}. {source}: {preview}")
                
            except Exception as e:
                print(f"Error: {e}")
                print("Make sure Ollama is running with: ollama serve")
                
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Setup failed: {e}")
        print("Troubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Make sure DeepSeek model is available: ollama pull deepseek-r1:8b")
        print("3. Check your internet connection for document loading")

if __name__ == "__main__":
    main()
