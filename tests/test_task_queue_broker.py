from unittest.mock import patch
import pytest
from app.core.celery_app import celery_app

def test_celery_task_queue_broker_dispatch():
    with patch.object(celery_app, "send_task") as mock_send_task:
        mock_send_task.return_value = None
        celery_app.send_task("process_ai_task", args=["test-id", "contract_analysis", {}])
        mock_send_task.assert_called_once_with("process_ai_task", args=["test-id", "contract_analysis", {}])
