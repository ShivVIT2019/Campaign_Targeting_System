import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] == True

def test_predict_endpoint():
    """Test prediction with valid data"""
    payload = {
        "Administrative": 2,
        "Administrative_Duration": 10.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 5,
        "ProductRelated_Duration": 100.0,
        "BounceRates": 0.02,
        "ExitRates": 0.05,
        "PageValues": 10.0,
        "SpecialDay": 0.0,
        "Month": "May",
        "OperatingSystems": "2",
        "Browser": "2",
        "Region": "1",
        "TrafficType": "2",
        "VisitorType": "Returning_Visitor",
        "Weekend": False
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "probability" in data
    assert "decision" in data
    assert 0 <= data["probability"] <= 1
    assert data["decision"] in ["TARGET", "DO_NOT_TARGET"]

def test_metrics_endpoint():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
