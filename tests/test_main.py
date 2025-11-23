from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test that the API is running"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

def test_evaluate_empty_answer():
    """Test that empty answers return an error (Validation Check)"""
    response = client.post("/evaluate-answer", json={"answer": ""})
    assert response.status_code == 400

# Note: We don't test the actual OpenAI call here to avoid spending money 
# every time we run tests. In a real job, we would 'mock' that connection.
