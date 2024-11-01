import pathway as pw
from pathway.xpacks.llm.llms import LiteLLMChat, prompt_chat_single_qa
from pathway.stdlib.ml.index import KNNIndex
from pathway.xpacks.llm.embedders import SentenceTransformerEmbedder
import os
from dotenv import load_dotenv

load_dotenv()
print("Environment variables loaded")

class RAGApplication:
    def __init__(self):
        print("Initializing RAG Application...")
        
        # Debug: Print the documents path
        docs_path = os.getenv("DOCUMENTS_PATH")
        print(f"Loading documents from: {docs_path}")
        
        # Initialize the LLM using LiteLLM for Ollama
        self.llm = LiteLLMChat(
            model="ollama/mistral",  # Using ollama prefix for LiteLLM
            api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.05,
            retry_strategy=pw.udfs.FixedDelayRetryStrategy(),
            cache_strategy=pw.udfs.DefaultCache(),
        )
        print("LLM initialized")
        
        # Initialize documents table with CSV format
        class DocumentSchema(pw.Schema):
            content: str
            
        self.documents = pw.io.csv.read(
            docs_path,
            schema=DocumentSchema,
            mode="streaming",
            csv_settings=pw.io.csv.CsvParserSettings(
                delimiter=",",
                quote='"',
                escape=None,
                enable_double_quote_escapes=True,
                enable_quoting=True,
                comment_character=None,
            )
        )
        print(f"Documents loaded from: {docs_path}")
        
        # Create embeddings using SentenceTransformers
        self.embedder = SentenceTransformerEmbedder(
            model="all-MiniLM-L6-v2",  # Using a lightweight model
        )
        
        # Create document embeddings
        self.enriched_documents = self.documents + self.documents.select(
            data=self.embedder(pw.this.content)
        )
        print("Document embeddings created")
        
    def setup_pipeline(self):
        print("\nSetting up pipeline...")
        
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
        
        # Create KNN index and process queries
        print("Setting up query processing pipeline...")
        index = KNNIndex(
            self.enriched_documents.data, 
            self.enriched_documents,
            n_dimensions=384  # Changed to match all-MiniLM-L6-v2 dimensions
        )
        
        # Embed queries
        embedded_queries = queries + queries.select(
            data=self.embedder(pw.this.text)
        )
        
        # Get relevant documents (updated to use content)
        query_context = embedded_queries + index.get_nearest_items(
            embedded_queries.data, 
            k=3, 
            collapse_rows=True
        ).select(documents_list=pw.this.content)  # changed from doc to content
        
        # Build prompts and get responses
        @pw.udf
        def build_prompt(documents, query) -> str:
            docs_str = "\n".join([str(doc) for doc in documents])  # ensure strings
            return f"Given the following documents:\n{docs_str}\nanswer this query: {query}"
        
        results = query_context.select(
            result=self.llm(
                prompt_chat_single_qa(
                    build_prompt(pw.this.documents_list, pw.this.text)
                )
            )
        )
        print("Query processing pipeline created")
        
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