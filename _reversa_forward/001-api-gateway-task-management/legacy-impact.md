# Impacto no Legado: API Gateway & Gerenciamento de Tarefas Assíncronas

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  
> Nota de Âncora: Feature greenfield, sem legado pré-existente. Âncora: `prd.md` + specs SDD em `_reversa_sdd/sdd/`.  
> Estado do Reversa Config: `allowLegacyEdits: true`, liberação de escrita ativada.  

---

## 1. Mapeamento de Componentes Criados

| Arquivo Afetado | Componente SDD | Tipo | Severidade | Justificativa |
|-----------------|----------------|------|------------|---------------|
| `app/main.py` | `api-gateway-task-management` | componente-novo | LOW | Entrypoint FastAPI com middleware de 10MB |
| `app/api/v1/endpoints/tasks.py` | `api-gateway-task-management` | componente-novo | LOW | Endpoints HTTP POST /tasks e GET /tasks/{task_id} |
| `app/schemas/task.py` | `api-gateway-task-management` | componente-novo | LOW | Schemas Pydantic v2 de validação |
| `app/models/task.py` | `postgres-persistence-container` | componente-novo | LOW | Modelo ORM SQLAlchemy da tabela `tasks` |
| `app/core/celery_app.py` | `task-queue-broker` | componente-novo | LOW | Instância e broker Celery |
| `app/worker.py` | `ai-agent-orchestrator-validator` | componente-novo | LOW | Worker de processamento assíncrono |
| `alembic/versions/001_create_tasks_table.py` | `postgres-persistence-container` | componente-novo | LOW | Migration inicial da tabela `tasks` |
| `docker-compose.yml` | `architecture.md` | componente-novo | LOW | Orquestração da stack Docker |

---

## 2. Seção "Preservadas"

> Feature greenfield. Nenhuma regra de legado pré-existente afetada.

---

## 3. Seção "Modificadas"

> Nenhuma regra modificada (criação inicial do projeto).
