import requests
import json

class Llama3Adapter:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def generate_answer(self, context: str, question: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama3",
            "prompt": f"{context}\n\nQ: {question}\nA:"
        }

        response = requests.post(f"{self.api_url}/api/generate", json=data, headers=headers, stream=True)

        if response.status_code != 200:
            raise Exception(f"Failed to get response from Llama API: {response.status_code}")

        response_text = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                response_text += chunk.decode('utf-8')

        # Split the response text into JSON objects and parse the last one
        try:
            response_json = json.loads(response_text.strip().split('\n')[-1])
            return response_json["response"]
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON response: {e}")
