from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskAcceptedResponse, TaskResponse
from app.core.celery_app import celery_app

router = APIRouter()

@router.post(
    "/tasks",
    response_model=TaskAcceptedResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submeter tarefa de IA assíncrona",
    description="Recebe o payload da tarefa de IA, valida via Pydantic, enfileira no Redis/Celery e retorna HTTP 202 com task_id."
)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    # Criar registro de tarefa no banco PostgreSQL com status 'queued'
    db_task = Task(
        task_type=task_in.task_type,
        status="queued",
        payload=task_in.payload
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    # Despachar mensagem para a fila Celery
    try:
        celery_app.send_task(
            "process_ai_task",
            args=[str(db_task.id), db_task.task_type, db_task.payload]
        )
    except Exception as e:
        # Registrar falha se houver erro ao conectar com o broker
        db_task.status = "failed"
        db_task.error_message = f"Falha ao despachar tarefa para o broker Redis: {str(e)}"
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enfileirar tarefa de IA no broker."
        )

    return TaskAcceptedResponse(
        task_id=db_task.id,
        status="queued",
        message="Tarefa recebida e enfileirada com sucesso."
    )

@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Consultar status e resultado de uma tarefa",
    description="Retorna o estado atualizado (queued, processing, completed, failed) e o resultado estruturado da execução."
)
async def get_task_status(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalars().first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa com o ID informado não foi encontrada."
        )

    return TaskResponse(
        task_id=db_task.id,
        task_type=db_task.task_type,
        status=db_task.status,
        payload=db_task.payload,
        result=db_task.result,
        error_message=db_task.error_message,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )
