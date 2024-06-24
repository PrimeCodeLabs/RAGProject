from pydantic import BaseModel
from typing import List, Dict

class Query(BaseModel):
    question: str

class RetrievedDocument(BaseModel):
    title: str
    date: str
    content: str

class Response(BaseModel):
    answer: str
    retrieved_documents: List[RetrievedDocument]
