import pathway as pw
from pathlib import Path
import os

class DocumentIndexer:
    def __init__(self, documents_path: str, embedding_handler):
        print(f"\nInitializing DocumentIndexer with path: {documents_path}")
        self.documents_path = documents_path
        self.embedding_handler = embedding_handler
        
    def index_documents(self):
        print("\nStarting document indexing...")
        print(f"Reading documents from: {self.documents_path}")
        
        # Create Pathway's real-time document indexing pipeline
        docs = pw.io.fs.read(
            self.documents_path,
            format="plaintext",
            mode="streaming",
            with_metadata=True,
            autocommit_duration_ms=1000
        )
        print("Document reader created")
        
        # Generate embeddings - embedding_handler already returns a list
        print("Generating embeddings for documents...")
        embedded_docs = docs.select(
            content=pw.this.data,
            embedding=pw.apply(self.embedding_handler, pw.this.data)  # Removed .tolist()
        )
        print("Document embeddings generated")
        
        return embedded_docs