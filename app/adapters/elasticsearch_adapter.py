import requests
from app.config import Config

class ElasticsearchAdapter:
    def __init__(self):
        self.url = Config.ELASTICSEARCH_URL

    def retrieve_documents(self, query: str):
        response = requests.post(f"{self.url}/_search", json={"query": {"match": {"content": query}}})
        response.raise_for_status()
        hits = response.json()['hits']['hits']
        return [hit['_source']['content'] for hit in hits]
