# app/core/services.py
from app.adapters.elasticsearch_adapter import ElasticsearchAdapter
from app.adapters.llama3_adapter import Llama3Adapter
from app.core.models import Query, Response, RetrievedDocument  # Ensure RetrievedDocument is imported
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, es_adapter: ElasticsearchAdapter, llama_adapter: Llama3Adapter):
        self.es_adapter = es_adapter
        self.llama_adapter = llama_adapter
        self.context_mapping = {
            "finance": ["stock", "investment", "financial", "market"],
            "law": ["legal", "court", "lawyer", "case"],
            "technology": ["tech", "AI", "artificial intelligence", "machine learning", "deep learning", "software", "hardware", "robotics", "automation", "data science"],
            "general": []
        }

    def determine_context(self, question: str) -> str:
        for context, keywords in self.context_mapping.items():
            if any(keyword.lower() in question.lower() for keyword in keywords):
                return f"This context is about {context}."
        return "This context is about general."

    def retrieve_documents(self, question: str):
        response = self.es_adapter.search_documents(question)
        documents = [RetrievedDocument(**hit["_source"]) for hit in response["hits"]["hits"]]
        logger.info(f"Retrieved documents: {documents}")
        return documents

    def answer_question(self, query: Query):
        question = query.question
        logger.info(f"Answering question: {question}")
        context = self.determine_context(question)
        logger.info(f"Determined context: {context}")
        retrieved_documents = self.retrieve_documents(question)
        document_contents = [doc.content for doc in retrieved_documents]
        
        context_with_documents = f"{context}\n\n" + "\n\n".join(document_contents)
        answer_text = self.llama_adapter.generate_answer(context_with_documents, question)
        return Response(answer=answer_text, retrieved_documents=retrieved_documents)
