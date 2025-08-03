from typing import Dict, List
from langchain import hub
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RAGChain:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        self.prompt = self._get_prompt()
        self.chain = self._build_chain()

    def _get_prompt(self):
        try:
            prompt = hub.pull("rlm/rag-prompt")
            print("Loaded RAG prompt from LangChain hub")
            return prompt
        except Exception as e:
            print(f"Using optimized prompt: {e}")
            template = """You are a helpful Bajaj Finserv policy expert assistant. Always provide a useful and informative answer to customer questions about insurance policies, loans, and financial products.

Available Context: {context}

Customer Question: {question}

Instructions:
- Use the provided context as your primary source of information
- If the exact information isn't in the context, provide general knowledge about the topic as it relates to Bajaj Finserv services
- Always give a helpful answer - never say information is not available
- Focus on being helpful, professional, and informative
- Provide exactly 2 paragraphs maximum
- Use clear, simple language that customers can understand

Helpful Professional Answer:"""
            return PromptTemplate.from_template(template)

    def _build_chain(self):
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain

    def invoke(self, question: str) -> Dict:
        try:
            retrieved_docs = self.retriever.get_relevant_documents(question)
            answer = self.chain.invoke(question)
            
            return {
                "question": question,
                "answer": answer,
                "source_documents": retrieved_docs
            }
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error generating response: {e}",
                "source_documents": []
            }

    def get_relevant_documents(self, question: str) -> List[Document]:
        return self.retriever.get_relevant_documents(question)
