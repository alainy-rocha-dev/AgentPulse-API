import pytest
from app.core.config import settings
from app.models.task import Task

def test_database_settings_urls():
    assert "postgresql+asyncpg://" in settings.ASYNC_DATABASE_URL
    assert "postgresql://" in settings.SYNC_DATABASE_URL
    assert settings.POSTGRES_DB == "automacao_agentes"

def test_task_model_definition():
    assert Task.__tablename__ == "tasks"
    assert hasattr(Task, "id")
    assert hasattr(Task, "task_type")
    assert hasattr(Task, "status")
    assert hasattr(Task, "payload")
    assert hasattr(Task, "result")
    assert hasattr(Task, "error_message")
    assert hasattr(Task, "created_at")
    assert hasattr(Task, "updated_at")

def test_task_model_to_dict():
    task = Task(
        task_type="code_generation",
        status="queued",
        payload={"prompt": "create a function"}
    )
    dict_repr = task.to_dict()
    assert dict_repr["task_type"] == "code_generation"
    assert dict_repr["status"] == "queued"
    assert dict_repr["payload"] == {"prompt": "create a function"}
