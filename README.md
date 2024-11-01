# PathwayRAG - Private Document Question Answering System

## Overview
PathwayRAG is a sophisticated local RAG (Retrieval-Augmented Generation) system built with Pathway and Ollama. It enables real-time document querying with context-aware AI responses while maintaining complete data privacy by processing everything locally.

## Key Features
- **Local Processing**: All computations happen on your machine
- **Real-time Document Indexing**: Automatic processing of document updates
- **Semantic Search**: Advanced document retrieval using embeddings
- **Context-Aware Responses**: AI-generated answers based on document context
- **REST API Interface**: Easy integration with other applications

## Technical Architecture

### Core Components
1. **RAG Application** (main.py)
   - Orchestrates the entire pipeline
   - Handles document indexing and query processing
   - Manages REST API endpoints

2. **Document Indexer** (indexer.py)
   - Real-time document monitoring and processing
   - Streaming support for continuous updates
   - Embedding generation for documents

3. **Embedding Handler** (embeddings.py)
   - Uses SentenceTransformer for semantic embeddings
   - Vectorizes both documents and queries
   - Supports batch processing

4. **LLM Integration** (llm.py)
   - Ollama integration for local LLM deployment
   - Context-aware prompt formatting
   - Asynchronous response generation

## Prerequisites

### System Requirements
- Python 3.10+
- 16GB RAM (minimum)
- [Ollama](https://ollama.ai) installed
- SentenceTransformer compatible GPU (optional)

### Dependencies
```bash
pip install pathway
pip install sentence-transformers
pip install python-dotenv
pip install fastapi
pip install uvicorn
```

## Setup and Installation

1. Clone the repository
```bash
git clone [repository-url]
cd pathwayrag
```

2. Create and configure environment variables
```bash
cp .env.example .env
```

Configure the following in `.env`:
```env
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=mistral
DOCUMENTS_PATH=/path/to/your/documents
```

3. Start Ollama and pull the Mistral model
```bash
ollama run mistral
```

4. Run the application
```bash
python src/main.py
```

## Running the Application

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv

# On Linux/MacOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Ollama Service
```bash
# Terminal 1: Start Ollama
ollama serve

# Verify Mistral model is available
ollama pull mistral
```

### 3. Prepare Test Documents
```bash
# Create documents directory if it doesn't exist
mkdir -p data/documents

# Add sample document
cat > data/documents/sample.txt << EOL
Pathway is a real-time data processing framework that enables developers to build robust data pipelines. 
It excels in handling streaming data and provides powerful capabilities for building real-time AI applications.
Some key features of Pathway include:
1. Real-time data processing
2. Built-in support for AI/ML workflows
3. Scalable architecture
4. Easy integration with various data sources
EOL
```

### 4. Launch Application
```bash
# Terminal 2: Start the main Pathway application
python src/main.py

# Terminal 3: Start the API server
python src/api.py
```

### 5. Test the System

#### Using curl:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"text": "What are the main features of Pathway?"}'
```

#### Using Python:
```python
import requests

# Send a test query
response = requests.post(
    "http://localhost:8000/query",
    json={"text": "What are the main features of Pathway?"}
)

# Print the response
print(response.json())
```

### Expected Output
```json
{
    "response": "Based on the context, the main features of Pathway include: 1. Real-time data processing, 2. Built-in support for AI/ML workflows, 3. Scalable architecture, and 4. Easy integration with various data sources. The framework is designed to enable developers to build robust data pipelines and excels in handling streaming data for real-time AI applications.",
    "status": "success"
}
```

### Troubleshooting

1. **Ollama Connection Issues**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/version
   
   # Restart Ollama if needed
   ollama serve
   ```

2. **Model Loading Issues**
   ```bash
   # Verify Mistral model
   ollama list
   
   # Pull model if missing
   ollama pull mistral
   ```

3. **API Connection Issues**
   ```bash
   # Check if API is running
   curl http://localhost:8000/health
   
   # Check application logs in Terminal 2 and 3
   ```

## API Usage

### Query Endpoint
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"text": "your question here"}'
```

## Project Structure
```
├── src/
│   ├── main.py          # Application entry point
│   ├── api.py           # FastAPI endpoints
│   ├── embeddings.py    # Embedding generation
│   ├── indexer.py       # Document processing
│   └── llm.py           # Ollama integration
├── .env                 # Environment variables
└── README.md           # Documentation
```

## How It Works

1. **Document Processing**
   - Documents are monitored in the specified directory
   - Text is extracted and embedded using SentenceTransformer
   - Embeddings are stored in memory for quick retrieval

2. **Query Processing**
   - User queries are received via REST API
   - Query is embedded and compared with document embeddings
   - Most relevant documents are retrieved (cosine similarity > 0.7)
   - Context and query are sent to LLM for response generation

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License

## Acknowledgments
- [Pathway](https://pathway.com) for the real-time processing framework
- [Ollama](https://ollama.ai) for local LLM capabilities
- [SentenceTransformers](https://www.sbert.net) for embedding generation