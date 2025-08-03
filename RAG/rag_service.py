from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import time
import logging
from typing import List, Dict
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8090').split(',')
CORS(app, origins=cors_origins)

logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

class RAGProcessor:
    def __init__(self):
        try:
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
            model_name = os.getenv('OLLAMA_MODEL', 'deepseek-r1:8b')
            
            # Optimize LLM settings for detailed responses
            self.llm = OllamaLLM(
                model=model_name, 
                base_url=ollama_url,
                temperature=0.2,        # Slightly higher for more creative responses
                top_p=0.95,            # Allow more diverse vocabulary
                num_ctx=4096,          # Larger context for more detailed responses
                num_predict=1024,      # Allow longer responses (4-6 paragraphs)
            )
            self.embeddings = OllamaEmbeddings(model=model_name, base_url=ollama_url)
            
            chunk_size = int(os.getenv('CHUNK_SIZE', '500'))
            chunk_overlap = int(os.getenv('CHUNK_OVERLAP', '100'))
            
            # Better chunking strategy for financial documents
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,     # Use environment variable
                chunk_overlap=chunk_overlap, # Use environment variable
                separators=["\n\n", "\n", ". ", " "],  # Better splitting points
                add_start_index=True,
                length_function=len
            )
            
            # Enhanced prompt for detailed responses
            self.prompt = PromptTemplate.from_template("""
You are a knowledgeable Bajaj Finserv policy expert assistant. Always provide comprehensive, detailed, and informative answers to customer questions about insurance policies, loans, and financial products.

Available Context:
{context}

Customer Question: {question}

Instructions:
- Use the provided context as your primary source of information
- If the exact information isn't in the context, supplement with relevant general knowledge about Bajaj Finserv services
- Always provide a detailed, helpful answer - never say information is not available
- Structure your response in 4-6 well-developed paragraphs
- Include specific details, examples, and practical information when possible
- Be professional, authoritative, and customer-focused
- Use clear language while being comprehensive
- Do not include reasoning or thinking tags in your response
- Cover different aspects of the topic to provide complete understanding
- When relevant, mention related Bajaj Finserv products or services

Detailed Professional Answer:""")
            
            logger.info("RAG Processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Processor: {e}")
            raise

    def clean_response(self, text: str) -> str:
        """Remove <think> tags and clean up the response"""
        # Remove <think>...</think> blocks (case insensitive, multiline)
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.IGNORECASE | re.DOTALL)
        # Clean up extra whitespace and normalize
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned.strip())
        # Split into paragraphs and limit to 2
        paragraphs = [p.strip() for p in cleaned.split('\n\n') if p.strip()]
        return '\n\n'.join(paragraphs[:2])

    def debug_retrieved_chunks(self, chunks: List, query: str):
        """Debug what chunks are being retrieved"""
        logger.info(f"🔍 Query: {query}")
        logger.info(f"📊 Retrieved {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks[:3]):  # Log top 3 chunks
            content_preview = chunk.page_content[:200].replace('\n', ' ')
            logger.info(f"📄 Chunk {i+1}: {content_preview}...")
            logger.info(f"📝 Source: {chunk.metadata.get('title', 'Unknown')}")

    def validate_context(self, context: str, query: str) -> bool:
        """Validate if context is relevant to the query"""
        if not context.strip():
            logger.warning("⚠️ Empty context provided")
            return False
            
        # Check for keyword overlap
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        
        # Remove common words
        common_words = {'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        query_words -= common_words
        context_words -= common_words
        
        overlap = len(query_words.intersection(context_words))
        relevance_score = overlap / len(query_words) if query_words else 0
        
        logger.info(f"📈 Context relevance score: {relevance_score:.2f}")
        return True  # Always return True since we want to provide an answer

    def filter_relevant_chunks(self, chunks: List, query: str, max_chunks: int = 3):
        """Filter and return most relevant chunks"""
        if not chunks:
            logger.warning("⚠️ No chunks available for filtering")
            return []
            
        # For now, return top chunks (Chroma already sorts by relevance)
        filtered = chunks[:max_chunks]
        
        logger.info(f"🎯 Filtered to {len(filtered)} most relevant chunks")
        return filtered

    def validate_context(self, context: str, query: str) -> bool:
        """Validate if context is relevant to the query"""
        if not context.strip():
            logger.warning("⚠️ Empty context provided")
            return False
            
        # Check for keyword overlap
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        
        # Remove common words
        common_words = {'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        query_words -= common_words
        context_words -= common_words
        
        overlap = len(query_words.intersection(context_words))
        relevance_score = overlap / len(query_words) if query_words else 0
        
        logger.info(f"📈 Context relevance score: {relevance_score:.2f}")
        
        if relevance_score < 0.1:  # Less than 10% overlap
            logger.warning(f"⚠️ Low relevance score: {relevance_score:.2f}")
        
        return relevance_score > 0.05  # At least 5% overlap

    def filter_relevant_chunks(self, chunks: List, query: str, max_chunks: int = 3):
        """Filter and return most relevant chunks"""
        if not chunks:
            return []
            
        # For now, return top chunks (Chroma already sorts by relevance)
        # In future, can add more sophisticated filtering
        filtered = chunks[:max_chunks]
        
        logger.info(f"🎯 Filtered to {len(filtered)} most relevant chunks")
        return filtered

    def process_documents(self, documents: List[Dict]) -> List[Document]:
        """Process and validate documents with enhanced debugging"""
        langchain_docs = []
        
        for i, doc in enumerate(documents):
            if not doc.get('content', '').strip():
                logger.warning(f"⚠️ Document {i+1} has empty content")
                continue
                
            content = doc['content'].strip()
            langchain_doc = Document(
                page_content=content,
                metadata={
                    'title': doc.get('title', f'Document_{i+1}'),
                    'file_type': doc.get('file_type', 'unknown'),
                    'content_length': len(content)
                }
            )
            langchain_docs.append(langchain_doc)
            
            # Debug document processing
            logger.info(f"📄 Processed: {doc.get('title', f'Doc_{i+1}')} ({len(content)} chars)")
        
        if not langchain_docs:
            logger.error("❌ No valid documents to process")
            return []
        
        chunks = self.text_splitter.split_documents(langchain_docs)
        logger.info(f"✂️ Created {len(chunks)} chunks from {len(langchain_docs)} documents")
        
        # Validate chunk quality
        for i, chunk in enumerate(chunks[:3]):  # Check first 3 chunks
            logger.info(f"🔤 Chunk {i+1} preview: {chunk.page_content[:100]}...")
            
        return chunks

    def create_vector_store(self, documents: List[Document]):
        try:
            persist_dir = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
            vector_store = Chroma.from_documents(
                documents, 
                self.embeddings,
                persist_directory=persist_dir
            )
            logger.info("Vector store created successfully")
            return vector_store
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise

    def query(self, question: str, documents: List[Dict]) -> Dict:
        start_time = time.time()
        try:
            logger.info(f"🚀 Starting RAG query: {question[:50]}...")
            
            if not documents:
                return {
                    "answer": "I'd be happy to help you with your Bajaj Finserv related questions! However, I need some documents to be uploaded first to provide you with accurate and specific information about policies, loans, or insurance products.",
                    "source_documents": []
                }

            # Step 1: Document processing with timing
            doc_start = time.time()
            doc_chunks = self.process_documents(documents)
            doc_time = time.time() - doc_start
            logger.info(f"📄 Document processing: {doc_time:.2f}s")
            
            if not doc_chunks:
                return {
                    "answer": "I'm here to help with your Bajaj Finserv questions! While I couldn't extract specific content from the uploaded documents, I can still provide general guidance about our policies, loans, and insurance products. Please feel free to ask your question.",
                    "source_documents": []
                }

            # Step 2: Vector store creation with timing
            vector_start = time.time()
            vector_store = self.create_vector_store(doc_chunks)
            vector_time = time.time() - vector_start
            logger.info(f"🧠 Vector store creation: {vector_time:.2f}s")
            
            # Step 3: Document retrieval with timing
            retrieval_start = time.time()
            max_docs = min(int(os.getenv('MAX_DOCUMENTS_PER_QUERY', '6')), len(doc_chunks))
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": max_docs}
            )

            retrieved_docs = retriever.invoke(question)
            self.debug_retrieved_chunks(retrieved_docs, question)
            
            # Filter most relevant chunks
            filtered_docs = self.filter_relevant_chunks(retrieved_docs, question, max_chunks=3)
            retrieval_time = time.time() - retrieval_start
            logger.info(f"🔍 Document retrieval: {retrieval_time:.2f}s")

            def format_docs(docs):
                if not docs:
                    return "General knowledge about Bajaj Finserv products and services."
                context = "\n\n".join(doc.page_content for doc in docs)
                return context

            # Validate context but always proceed
            context = format_docs(filtered_docs)
            self.validate_context(context, question)

            # Step 4: LLM Generation with timing
            gen_start = time.time()
            chain = (
                {"context": lambda x: context, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

            logger.info("🤖 Generating response...")
            answer = chain.invoke(question)
            
            # Clean the response to remove <think> tags and limit to 2 paragraphs
            cleaned_answer = self.clean_response(answer)
            gen_time = time.time() - gen_start
            logger.info(f"🤖 LLM generation: {gen_time:.2f}s")

            # Extract source documents (limit to top 3)
            source_documents = []
            for doc in filtered_docs:
                title = doc.metadata.get('title', 'Unknown Document')
                if title not in source_documents:
                    source_documents.append(title)

            total_time = time.time() - start_time
            logger.info(f"⚡ Total processing time: {total_time:.2f}s")
            logger.info(f"✅ Successfully processed query with {len(source_documents)} sources")
            
            return {
                "answer": cleaned_answer,
                "source_documents": source_documents[:3],  # Limit to 3 sources
                "processing_time": {
                    "total": round(total_time, 2),
                    "document_processing": round(doc_time, 2),
                    "vector_store": round(vector_time, 2),
                    "retrieval": round(retrieval_time, 2),
                    "generation": round(gen_time, 2)
                }
            }

        except Exception as e:
            total_time = time.time() - start_time
            logger.error(f"❌ Error processing query after {total_time:.2f}s: {e}")
            return {
                "answer": "I'm here to help with your Bajaj Finserv questions! While I encountered a technical issue processing your specific request, I can still assist you with general information about our policies, loans, and insurance products. Please try asking your question in a different way.",
                "source_documents": [],
                "error": str(e),
                "processing_time": {"total": round(total_time, 2)}
            }

try:
    rag_processor = RAGProcessor()
    logger.info("RAG service ready")
except Exception as e:
    logger.error(f"Failed to initialize RAG service: {e}")
    rag_processor = None

@app.route('/health', methods=['GET'])
def health():
    if rag_processor is None:
        return jsonify({"status": "error", "message": "RAG processor not initialized"}), 500
    
    try:
        test_response = rag_processor.llm.invoke("Hello")
        return jsonify({"status": "ok", "ollama_connected": True})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Ollama connection failed: {e}"}), 500

@app.route('/rag/query', methods=['POST'])
def rag_query():
    if rag_processor is None:
        return jsonify({"error": "RAG service not available"}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        documents = data.get('documents', [])
        
        logger.info(f"Processing query: {query[:50]}... with {len(documents)} documents")
        
        result = rag_processor.query(query, documents)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in rag_query endpoint: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
    flask_port = int(os.getenv('FLASK_PORT', '8080'))
    flask_debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting RAG Python service on {flask_host}:{flask_port}")
    print("Make sure Ollama is running with: ollama serve")
    print(f"Make sure {os.getenv('OLLAMA_MODEL', 'deepseek-r1:8b')} model is available")
    app.run(host=flask_host, port=flask_port, debug=flask_debug)
