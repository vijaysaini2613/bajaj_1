import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Document Q&A System" in data["message"]

def test_hackrx_endpoint_without_auth():
    """Test the main endpoint without authentication"""
    test_request = {
        "documents": [
            {"type": "text", "content": "This is a test document with coverage limits of $100,000."}
        ],
        "questions": ["What is the coverage limit?"]
    }
    
    response = client.post("/hackrx/run", json=test_request)
    assert response.status_code == 401  # Should require authentication

def test_hackrx_endpoint_with_invalid_auth():
    """Test the main endpoint with invalid authentication"""
    test_request = {
        "documents": [
            {"type": "text", "content": "This is a test document with coverage limits of $100,000."}
        ],
        "questions": ["What is the coverage limit?"]
    }
    
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/hackrx/run", json=test_request, headers=headers)
    assert response.status_code == 401

def test_invalid_document_type():
    """Test with invalid document type"""
    test_request = {
        "documents": [
            {"type": "invalid", "content": "Test content"}
        ],
        "questions": ["Test question?"]
    }
    
    response = client.post("/hackrx/run", json=test_request)
    assert response.status_code == 422  # Validation error

def test_empty_questions():
    """Test with empty questions list"""
    test_request = {
        "documents": [
            {"type": "text", "content": "Test content"}
        ],
        "questions": []
    }
    
    response = client.post("/hackrx/run", json=test_request)
    assert response.status_code == 422  # Validation error

def test_empty_documents():
    """Test with empty documents list"""
    test_request = {
        "documents": [],
        "questions": ["Test question?"]
    }
    
    response = client.post("/hackrx/run", json=test_request)
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__])
