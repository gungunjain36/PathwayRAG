import requests
import time

def test_direct_pathway():
    """Test Pathway endpoint directly"""
    response = requests.post(
        "http://localhost:3000/",
        json={"text": "What are the main features of Pathway?"}
    )
    print("\nDirect Pathway Response:", response.json())

def test_via_fastapi():
    """Test through FastAPI endpoint"""
    response = requests.post(
        "http://localhost:8000/query",
        json={"text": "What are the main features of Pathway?"}
    )
    print("\nFastAPI Response:", response.json())

if __name__ == "__main__":
    # Wait for servers to start
    print("Waiting for servers to start...")
    time.sleep(5)
    
    print("\nTesting Direct Pathway Endpoint...")
    test_direct_pathway()
    
    print("\nTesting FastAPI Endpoint...")
    test_via_fastapi() 
    
    