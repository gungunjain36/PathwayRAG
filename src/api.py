from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/query")
async def query_documents(query: Query):
    try:
        # Forward the request to Pathway's REST connector
        response = requests.post(
            "http://localhost:3000/",  # Pathway's endpoint
            json={"text": query.text}
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Changed port to 8000