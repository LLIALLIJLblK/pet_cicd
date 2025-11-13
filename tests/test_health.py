
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "pet_shop"}

def test_readiness_check():
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "service": "pet_shop"}