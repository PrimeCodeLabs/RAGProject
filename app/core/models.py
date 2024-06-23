from pydantic import BaseModel
from typing import List

class Query(BaseModel):
    question: str

class Response(BaseModel):
    retrieved_documents: List[str]
    answer: str