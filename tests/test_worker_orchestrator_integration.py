from unittest.mock import patch, MagicMock
from app.worker import process_ai_task
from app.schemas.agent_output import AnalysisOutputSchema, MetricsSchema, MetadataSchema
from app.services.repair_loop import SchemaValidationError

@patch("app.worker.get_sync_db_connection")
@patch("app.worker.AgentOrchestrator")
def test_process_ai_task_success(mock_orchestrator_cls, mock_db_conn):
    # Mock do Banco
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    # Mock do Orquestrador
    mock_instance = MagicMock()
    mock_orchestrator_cls.return_value = mock_instance
    mock_instance.run_task.return_value = AnalysisOutputSchema(
        summary="Tarefa executada via worker",
        key_findings=["Finding 1"],
        metrics=MetricsSchema(total_score=95.0, risk_level="LOW", calculated_items=1),
        metadata=MetadataSchema(repair_attempts=0, execution_time_seconds=0.1, model_used="test")
    )

    result = process_ai_task("task-123", "contract_analysis", {"test": "data"})

    assert result["summary"] == "Tarefa executada via worker"
    assert result["metrics"]["total_score"] == 95.0
    assert mock_cur.execute.call_count >= 2  # processing e completed

@patch("app.worker.get_sync_db_connection")
@patch("app.worker.AgentOrchestrator")
def test_process_ai_task_schema_validation_error(mock_orchestrator_cls, mock_db_conn):
    # Mock do Banco
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    # Mock do Orquestrador lançando erro de schema
    mock_instance = MagicMock()
    mock_orchestrator_cls.return_value = mock_instance
    mock_instance.run_task.side_effect = SchemaValidationError("SchemaValidationError: Falha após 3 tentativas")

    result = process_ai_task("task-456", "contract_analysis", {"test": "data"})

    assert result["status"] == "failed"
    assert "SchemaValidationError" in result["error"]
