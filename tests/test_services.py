# tests/test_services.py

import pytest
from unittest.mock import MagicMock
from app.core.services import RAGService
from app.core.models import Query, Response, RetrievedDocument

@pytest.fixture
def mock_es_adapter():
    return MagicMock()

@pytest.fixture
def mock_llama_adapter():
    return MagicMock()

@pytest.fixture
def rag_service(mock_es_adapter, mock_llama_adapter):
    return RAGService(es_adapter=mock_es_adapter, llama_adapter=mock_llama_adapter)

def test_determine_context(rag_service):
    assert rag_service.determine_context("What are the latest stock trends?") == "This context is about finance."
    assert rag_service.determine_context("Tell me about recent court cases.") == "This context is about law."
    assert rag_service.determine_context("What are the advancements in AI?") == "This context is about technology."
    assert rag_service.determine_context("How is the weather today?") == "This context is about general."

def test_retrieve_documents(rag_service, mock_es_adapter):
    # Mock the response from ElasticsearchAdapter
    mock_response = {
        "hits": {
            "hits": [
                {"_source": {"title": "Doc 1", "date": "2024-06-20", "content": "Doc 1 content"}},
                {"_source": {"title": "Doc 2", "date": "2024-06-21", "content": "Doc 2 content"}}
            ]
        }
    }
    mock_es_adapter.search_documents.return_value = mock_response

    # Call retrieve_documents
    question = "Tell me about AI advancements."
    documents = rag_service.retrieve_documents(question)

    # Check if documents are correctly retrieved
    expected_documents = [
        RetrievedDocument(title="Doc 1", date="2024-06-20", content="Doc 1 content"),
        RetrievedDocument(title="Doc 2", date="2024-06-21", content="Doc 2 content")
    ]
    assert documents == expected_documents

def test_answer_question(rag_service, mock_llama_adapter):
    # Mock the context determination
    question = "What are the latest trends in AI?"
    context = "This context is about technology."
    rag_service.determine_context = MagicMock(return_value=context)

    # Mock the document retrieval
    mock_documents = [
        RetrievedDocument(title="Doc 1", date="2024-06-20", content="Doc 1 content"),
        RetrievedDocument(title="Doc 2", date="2024-06-21", content="Doc 2 content")
    ]
    rag_service.retrieve_documents = MagicMock(return_value=mock_documents)

    # Mock the response from Llama3Adapter
    mock_llama_response = "The latest trends in AI include advancements in natural language processing."
    mock_llama_adapter.generate_answer.return_value = mock_llama_response

    # Call answer_question
    query = Query(question=question)
    response = rag_service.answer_question(query)

    # Check if the response is correctly formed
    assert response.answer == mock_llama_response
    assert response.retrieved_documents == mock_documents
