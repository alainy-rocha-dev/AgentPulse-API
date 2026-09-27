from uuid import UUID
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    task_type: str = Field(..., example="contract_analysis", description="Tipo da tarefa de IA")
    payload: Dict[str, Any] = Field(..., example={"contract_text": "Exemplo de contrato..."}, description="Payload de parâmetros da tarefa")

class TaskAcceptedResponse(BaseModel):
    task_id: UUID
    status: str = Field(default="queued")
    message: str = Field(default="Tarefa recebida e enfileirada com sucesso.")

class TaskResponse(BaseModel):
    task_id: UUID
    task_type: str
    status: str
    payload: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
