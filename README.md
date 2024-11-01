# PathwayRAG - Private Document Question Answering System

## Overview
PathwayRAG is a local RAG (Retrieval-Augmented Generation) system built with Pathway, Ollama, and Streamlit. It enables real-time document querying with context-aware AI responses while maintaining complete data privacy by processing everything locally.

## Key Features
- **Local Processing**: All computations happen on your machine
- **Interactive UI**: Built with Streamlit for easy interaction
- **Real-time Responses**: Instant answers to your queries
- **Semantic Search**: Advanced document retrieval using embeddings
- **Context-Aware Responses**: AI-generated answers based on document context

## Technical Stack
- **Pathway**: For real-time data processing and RAG pipeline
- **Ollama**: Local LLM hosting (Mistral model)
- **Streamlit**: Interactive web interface
- **SentenceTransformers**: Document and query embeddings

## Prerequisites

### System Requirements
- Python 3.10+
- [Ollama](https://ollama.ai) installed
- 8GB RAM (minimum)

### Dependencies
```bash
pip install -r requirements.txt
```

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/gungunjain36/PathwayRAG.git
```

2. Create virtual environment
```bash
python -m venv venv

# On Linux/MacOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create and configure environment variables
```bash
cp .env.example .env
```

Configure the following in `.env`:
```env
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=mistral
DOCUMENTS_PATH=./data/documents.csv
```

5. Prepare your documents
```bash
# Create a CSV file with your documents
python src/create_data.py
```

## Running the Application

1. Start Ollama and pull the Mistral model
```bash
# Terminal 1: Start Ollama
ollama serve

# Pull the model
ollama pull mistral
```

2. Start the RAG backend
```bash
# Terminal 2: Start the Pathway application
python src/main.py
```

3. Launch the Streamlit UI
```bash
# Terminal 3: Start the Streamlit interface
streamlit run src/ui.py
```

4. Access the application
Open your browser and go to:
```
http://localhost:8501
```

## Project Structure
```
├── src/
│   ├── main.py          # RAG pipeline implementation
│   ├── ui.py            # Streamlit user interface
│   └── create_data.py   # Data preparation script
├── data/
│   └── documents.csv    # Document storage
├── .env                 # Environment variables
└── README.md           # Documentation
```

## How It Works

1. **Document Processing**
   - Documents are read from the CSV file
   - Text is embedded using SentenceTransformers
   - KNN index is created for similarity search

2. **Query Processing**
   - User enters query through Streamlit UI
   - Query is embedded and compared with document embeddings
   - Most relevant documents are retrieved
   - Context and query are sent to Mistral LLM for response generation

3. **User Interface**
   - Clean chat interface with message history
   - Real-time response display
   - Option to clear chat history
   - Informative sidebar with system information

## Troubleshooting

1. **Ollama Connection Issues**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Restart Ollama if needed
ollama serve
```

2. **UI Connection Issues**
```bash
# Check if main.py is running (should be on port 3000)
curl http://localhost:3000

# Check if Streamlit is running (should be on port 8501)
curl http://localhost:8501
```

## License
MIT License

## Acknowledgments
- [Pathway](https://pathway.com) for the real-time processing framework
- [Ollama](https://ollama.ai) for local LLM capabilities
- [Streamlit](https://streamlit.io) for the user interface
- [SentenceTransformers](https://www.sbert.net) for embedding generation