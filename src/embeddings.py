from sentence_transformers import SentenceTransformer
import pathway as pw
import numpy as np

class EmbeddingHandler:
    def __init__(self, model_name):
        print(f"\nInitializing EmbeddingHandler with model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("SentenceTransformer model loaded")
    
    def get_embeddings(self, texts):
        print(f"\nGenerating embeddings for text: {texts[:100]}...")
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts)
        result = embeddings[0] if len(texts) == 1 else embeddings
        result_list = result.tolist()
        print(f"Embeddings generated with shape: {len(result_list)}")
        return result_list

    def __call__(self, texts):
        return self.get_embeddings(texts) 