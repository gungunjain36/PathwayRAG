import pathway as pw
import os
from dotenv import load_dotenv
from embeddings import EmbeddingHandler
from llm import OllamaLLM
from indexer import DocumentIndexer
import numpy as np

load_dotenv()
print("Environment variables loaded")

class RAGApplication:
    def __init__(self):
        print("Initializing RAG Application...")
        self.embedding_handler = EmbeddingHandler(os.getenv("EMBEDDING_MODEL_NAME"))
        print(f"Embedding model loaded: {os.getenv('EMBEDDING_MODEL_NAME')}")
        
        self.llm = OllamaLLM(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            model_name=os.getenv("MODEL_NAME")
        )
        print(f"LLM initialized with model: {os.getenv('MODEL_NAME')}")
        
        self.indexer = DocumentIndexer(
            documents_path=os.getenv("DOCUMENTS_PATH"),
            embedding_handler=self.embedding_handler
        )
        print(f"Document indexer initialized with path: {os.getenv('DOCUMENTS_PATH')}")
        
    def setup_pipeline(self):
        print("\nSetting up pipeline...")
        
        # Index documents
        print("Indexing documents...")
        embedded_docs = self.indexer.index_documents()
        print("Documents indexed successfully")
        
        # Query handling logic
        @pw.udf
        def query_processor(query: str, context: str) -> str:
            print(f"\nProcessing query: {query}")
            print(f"With context: {context}")
            response = self.llm.generate(query, context)
            print(f"Generated response: {response}")
            return response

        @pw.udf
        def compute_similarity(v1: list, v2: list) -> float:
            try:
                # Lists are already in the correct format
                dot_product = float(sum(a * b for a, b in zip(v1, v2)))
                norm1 = float(sum(x * x for x in v1)) ** 0.5
                norm2 = float(sum(x * x for x in v2)) ** 0.5
                
                if norm1 == 0 or norm2 == 0:
                    return 0.0
                
                similarity = dot_product / (norm1 * norm2)
                print(f"Computed similarity: {similarity}")
                return similarity
            except Exception as e:
                print(f"Error computing similarity: {e}")
                return 0.0
        
        print("UDFs defined successfully")
        
        # Define input schema
        class QuerySchema(pw.Schema):
            text: str
        print("Query schema defined")

        # Create HTTP input
        print("Setting up HTTP connector...")
        queries, response_writer = pw.io.http.rest_connector(
            host="0.0.0.0",
            port=3000,
            schema=QuerySchema,
            delete_completed_queries=True
        )
        print("HTTP connector created")
        
        # Process queries
        print("Setting up query processing pipeline...")
        query_embeddings = queries.select(
            query=pw.this.text,
            embedding=pw.apply(self.embedding_handler, pw.this.text)
        )
        print("Query embedding processor created")

        # Add a common key for joining
        print("Adding join keys...")
        docs_with_key = embedded_docs.select(
            join_key=1,  # Changed from 'id' to 'join_key'
            content=pw.this.content,
            embedding=pw.this.embedding
        )
        
        queries_with_key = query_embeddings.select(
            join_key=1,  # Changed from 'id' to 'join_key'
            query=pw.this.query,
            embedding=pw.this.embedding
        )

        # Join using the common key
        print("Computing similarities...")
        similarities = docs_with_key.join(
            queries_with_key,
            docs_with_key.join_key == queries_with_key.join_key  # Updated join condition
        ).select(
            content=docs_with_key.content,
            query=queries_with_key.query,
            score=pw.apply(
                compute_similarity,
                docs_with_key.embedding,
                queries_with_key.embedding
            )
        )
        print("Similarities computed")
        
        # Filter and reduce
        print("Setting up filtering and reduction...")
        filtered_docs = similarities.filter(
            pw.this.score > 0.7
        ).reduce(
            content=pw.reducers.max(pw.this.content),
            query=pw.reducers.max(pw.this.query)
        )
        print("Filtering and reduction pipeline created")
        
        # Generate response
        print("Setting up response generation...")
        results = filtered_docs.select(
            response=pw.apply(
                query_processor,
                pw.this.query,
                pw.this.content
            )
        )
        print("Response generation pipeline created")
        
        # Write results
        print("Setting up response writer...")
        response_writer(results)
        print("Response writer configured")
        
        return results

if __name__ == "__main__":
    print("\nStarting PathwayRAG application...")
    app = RAGApplication()
    print("\nInitializing pipeline...")
    results = app.setup_pipeline()
    print("\nStarting Pathway runtime...")
    pw.run()
    print("Application running!")