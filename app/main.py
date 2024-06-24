import asyncio
import logging
from app.adapters.elasticsearch_adapter import ElasticsearchAdapter
from app.adapters.llama3_adapter import Llama3Adapter
from fastapi import FastAPI
from app.core.services import RAGService
from app.core.models import Query, Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
es_adapter = ElasticsearchAdapter()
llama_adapter = Llama3Adapter(api_url="http://ollama:11434")
app = FastAPI()
rag_service = RAGService(
    es_adapter=es_adapter,
    llama_adapter=llama_adapter
)


@app.post("/ask", response_model=Response)
def ask_question(query: Query):
    try:
        result = rag_service.answer_question(query)
        return result
    except Exception as e:
        logger.error(f"Error in ask_question endpoint: {e}")
        return {"answer": "", "retrieved_documents": []}