import os

class Config:
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
    LLAMA3_API_URL = os.getenv('LLAMA3_API_URL', 'http://localhost:11434/api/generate')
