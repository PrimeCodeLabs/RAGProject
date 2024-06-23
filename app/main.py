import asyncio
from fastapi import FastAPI
from app.core.services import RAGService
from app.core.models import Query, Response

app = FastAPI()
rag_service = RAGService()

@app.post("/ask", response_model=Response)
def ask_question(query: Query):
    return rag_service.answer_question(query)