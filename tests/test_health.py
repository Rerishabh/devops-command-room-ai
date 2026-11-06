from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "system": "DevOps Command Room"}


def test_health_explicit_healthy(monkeypatch):
    monkeypatch.setenv("SERVICE_STATUS", "healthy")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "uptime_s": 3600}


def test_health_explicit_degraded(monkeypatch):
    monkeypatch.setenv("SERVICE_STATUS", "degraded")
    response = client.get("/health")
    assert response.status_code == 500
    assert response.json() == {"detail": "Service degraded: memory leak detected"}


def test_default_health_check_production_incident(monkeypatch):
    # Clear any ambient environment variable
    monkeypatch.delenv("SERVICE_STATUS", raising=False)
    response = client.get("/health")
    # Expected production contract: health check should return 200 OK
    # NOTE: This test will fail initially because default SERVICE_STATUS is degraded.
    # This represents the live incident for hackathon demonstration.
    assert response.status_code == 200

