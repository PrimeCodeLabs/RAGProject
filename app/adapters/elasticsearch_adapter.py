from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger(__name__)

class ElasticsearchAdapter:
    def __init__(self, url="http://elasticsearch:9200"):
        self.client = Elasticsearch(url)

    def search_documents(self, query):
        search_query = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }
        response = self.client.search(
            index="documents",
            body=search_query,
            headers={"Content-Type": "application/json"}
        )
        logger.info(f"Elasticsearch response: {response}")
        return response
