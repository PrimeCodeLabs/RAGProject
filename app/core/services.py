from app.adapters.llama3_adapter import Llama3Adapter
from elasticsearch import Elasticsearch

class RAGService:
    def __init__(self):
        self.es = Elasticsearch(
            ["http://elasticsearch:9200"]
        )
        self.llama_adapter = Llama3Adapter(api_url="http://ollama:11434")

    def retrieve_documents(self, query):
        response = self.es.search(
            index="documents",
            body={
                "query": {
                    "match": {
                        "content": query.question
                    }
                }
            },
            headers={"Content-Type": "application/json"}
        )
        print(response)
        return [hit["_source"] for hit in response["hits"]["hits"]]

    def answer_question(self, query):
        context = "some context"
        answer_text = self.llama_adapter.generate_answer(context, query.question)
        retrieved_documents = self.retrieve_documents(query)
        return {"answer": answer_text, "retrieved_documents": retrieved_documents}