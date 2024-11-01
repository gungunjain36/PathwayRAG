# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install pathway
pip install sentence-transformers
pip install fastapi
pip install uvicorn
pip install python-dotenv
pip install pydantic 