import requests
import json
import os
from typing import Optional

class OllamaLLM:
    def __init__(self, base_url: str, model_name: str):
        print(f"\nInitializing OllamaLLM with base_url: {base_url}")
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        print(f"Using model: {model_name}")

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        try:
            print(f"\nGenerating response for prompt: {prompt[:100]}...")
            if context:
                print(f"Using context: {context[:100]}...")
                prompt = f"""Context: {context}\n\nQuestion: {prompt}\n\nAnswer based on the context provided:"""
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            print("Sending request to Ollama...")
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()["response"]
            print(f"Generated response: {result[:100]}...")
            return result
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"Error: {error_msg}")
            return error_msg