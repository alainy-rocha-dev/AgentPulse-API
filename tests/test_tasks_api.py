import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app
from app.core.database import get_db

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@patch("app.api.v1.endpoints.tasks.celery_app.send_task")
def test_create_task_validation(mock_send_task):
    # Teste payload inválido (HTTP 422)
    response = client.post("/api/v1/tasks", json={})
    assert response.status_code == 422

def test_payload_too_large():
    # Teste payload maior que 10 MB (HTTP 413)
    large_payload = "a" * (10 * 1024 * 1024 + 100)
    response = client.post(
        "/api/v1/tasks",
        headers={"content-length": str(len(large_payload))},
        content=large_payload
    )
    assert response.status_code == 413

def test_get_nonexistent_task():
    async def mock_get_db():
        mock_session = AsyncMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = mock_get_db
    try:
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/tasks/{fake_uuid}")
        assert response.status_code == 404
        assert "não foi encontrada" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
