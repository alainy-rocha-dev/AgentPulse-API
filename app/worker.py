import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.agent_orchestrator import AgentOrchestrator
from app.services.repair_loop import SchemaValidationError

logger = logging.getLogger(__name__)

def get_sync_db_connection():
    return psycopg2.connect(settings.SYNC_DATABASE_URL)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(psycopg2.OperationalError)
)
def update_task_status_with_retry(conn, query, params):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        conn.commit()

@celery_app.task(name="process_ai_task", bind=True, max_retries=3)
def process_ai_task(self, task_id: str, task_type: str, payload: dict):
    """
    Worker Celery responsável por executar a cadeia de agentes de IA
    via AgentOrchestrator e persistir o resultado final ou erro no PostgreSQL.
    """
    logger.info(f"Consumindo mensagem para task_id={task_id}, type={task_type}")
    conn = get_sync_db_connection()
    try:
        # 1. Atualizar status para 'running'
        update_task_status_with_retry(
            conn,
            "UPDATE tasks SET status = %s, updated_at = NOW() WHERE id = %s",
            ("running", task_id)
        )
        logger.info(f"Task task_id={task_id} atualizada para status 'running'")

        # 2. Executar a cadeia de agentes de IA via Orquestrador com Repair Loop
        orchestrator = AgentOrchestrator()
        output_schema = orchestrator.run_task(task_type, payload)
        result_data = output_schema.model_dump()

        # 3. Persistir resultado final com status 'completed'
        update_task_status_with_retry(
            conn,
            "UPDATE tasks SET status = %s, result = %s, updated_at = NOW() WHERE id = %s",
            ("completed", json.dumps(result_data), task_id)
        )
        logger.info(f"Task task_id={task_id} concluída com sucesso (status 'completed')")
        return result_data

    except SchemaValidationError as val_err:
        conn.rollback()
        logger.error(f"Erro de validação de schema para task_id={task_id}: {val_err}")
        # Erro definitivo de schema após 3 tentativas: não retenta o Celery job
        update_task_status_with_retry(
            conn,
            "UPDATE tasks SET status = %s, error_message = %s, updated_at = NOW() WHERE id = %s",
            ("failed", str(val_err), task_id)
        )
        return {"status": "failed", "error": str(val_err)}

    except Exception as exc:
        conn.rollback()
        logger.error(f"Erro ao processar task_id={task_id}: {exc}")
        # Outros erros de infra/banco: registra status 'failed' e dispara retry Celery
        try:
            update_task_status_with_retry(
                conn,
                "UPDATE tasks SET status = %s, error_message = %s, updated_at = NOW() WHERE id = %s",
                ("failed", str(exc), task_id)
            )
        except Exception as db_exc:
            logger.error(f"Erro ao atualizar status de falha no banco para task_id={task_id}: {db_exc}")
        raise self.retry(exc=exc, countdown=5)
    finally:
        conn.close()
