import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

with patch("redis.Redis") as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_job_returns_job_id():
    with patch("main.r") as mock_r:
        mock_r.lpush.return_value = 1
        mock_r.hset.return_value = True
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()

def test_get_job_status():
    with patch("main.r") as mock_r:
        mock_r.hget.return_value = "queued"
        response = client.get("/jobs/test-job-id")
        assert response.status_code == 200
        assert response.json()["status"] == "queued"

def test_get_job_not_found():
    with patch("main.r") as mock_r:
        mock_r.hget.return_value = None
        response = client.get("/jobs/non-existent")
        assert response.status_code == 200
        assert response.json() == {"error": "not found"}
