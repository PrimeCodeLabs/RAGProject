# app/adapters/llama3_adapter.py
import requests
import logging

logger = logging.getLogger(__name__)

class Llama3Adapter:
    def __init__(self, api_url):
        self.api_url = api_url

    def generate_answer(self, context, question):
        payload = {
            "model": "llama3",
            "prompt": f"{context}\n\n{question}",
            "format": "json",
            "stream": False
        }
        try:
            logger.info(f"Sending payload to Llama API: {payload}")
            response = requests.post(f"{self.api_url}/api/generate", json=payload)
            response.raise_for_status()  # Raise an error for bad status codes
            logger.info(f"Received response from Llama API: {response.text}")
            response_data = response.json()
            raw_answer = response_data.get('response', '')
            # Clean up the response
            cleaned_answer = raw_answer.strip().strip('{}').strip()
            if not cleaned_answer:
                cleaned_answer = "No answer could be generated."
            return cleaned_answer
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {response.content}")
            raise
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
            raise
