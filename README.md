# ⚡ AgentPulse API

> **Asynchronous AI agent orchestration with validated LLM output**

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3%2B-green.svg)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-5.0%2B-red.svg)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791.svg)](https://www.postgresql.org/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-ready-2496ED.svg)](https://www.docker.com/)

AgentPulse is a backend for running **long AI agent tasks** without HTTP timeouts. A request returns immediately with `202 Accepted` and a `task_id`; the work runs in a **Celery + Redis** worker; the result is stored in **PostgreSQL** and fetched later by ID.

Its core feature is a **Pydantic repair loop**: when the LLM returns malformed or incomplete JSON, the validation error is sent back to the model so it can fix its own output — up to a fixed number of attempts. Numbers are computed by **deterministic Python tools**, not by the LLM.

It is also the execution layer of [FinAgent](https://github.com/alainy-rocha-dev/FinAgent).

---

## Architecture

```mermaid
flowchart TD
    Client([Client]) -->|1. POST /api/v1/tasks| API[FastAPI]
    API -->|2. 202 Accepted + task_id| Client
    API -->|3. enqueue| Redis[(Redis broker)]

    subgraph Background processing
        Redis -->|4. consume| Worker[Celery worker]
        Worker -->|5. deterministic tools| Tools[Risk score calculator]
        Worker -->|6. LLM call| Agent[Agent orchestrator]
        Agent -->|7. validate / repair| Repair[Pydantic repair loop]
    end

    Worker -->|8. save status + result| Postgres[(PostgreSQL)]
    Client -.->|"9. GET /api/v1/tasks/{task_id}"| API
    API -.-> Postgres
```

## The repair loop in action

The LLM must return JSON matching this schema:

```python
class AnalysisOutputSchema(BaseModel):
    summary: str
    key_findings: list[str]
    metrics: MetricsSchema      # total_score, risk_level, calculated_items
    metadata: MetadataSchema    # repair_attempts, execution_time_seconds, model_used
```

**Attempt 1** — the model forgets a required field:

```json
{"summary": "Missing metrics"}
```

Pydantic rejects it (`metrics: Field required`). The loop re-prompts the model with the original prompt **plus the exact validation error**, asking for valid JSON only.

**Attempt 2** — corrected output, accepted:

```json
{
  "summary": "Fixed on the 2nd attempt",
  "key_findings": ["OK"],
  "metrics": {"total_score": 80.0, "risk_level": "LOW", "calculated_items": 1},
  "metadata": {"repair_attempts": 1, "execution_time_seconds": 1.0, "model_used": "..."}
}
```

If every attempt fails, the task ends with a clear `SchemaValidationError` instead of saving invalid data. Each LLM call also has its own retry with exponential backoff (tenacity) for transient errors.

*(This exact scenario is covered by `tests/test_repair_loop.py`.)*

## API

| Method | Endpoint | Description | Status |
|---|---|---|---|
| `POST` | `/api/v1/tasks` | Submit a task for asynchronous execution | `202 Accepted` |
| `GET` | `/api/v1/tasks/{task_id}` | Get status (`queued`, `processing`, `completed`, `failed`) and result | `200 OK` |
| `GET` | `/` | Health check (service status and version) | `200 OK` |

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "contract_analysis", "payload": {"items": [{"issue": "No late-payment penalty", "severity": "HIGH"}]}}'
```

```json
{"task_id": "…", "status": "queued", "message": "Tarefa recebida e enfileirada com sucesso."}
```

Requests larger than 10 MB are rejected with `413`.

## Running

Requirements: Docker and Docker Compose.

```bash
git clone https://github.com/alainy-rocha-dev/AgentPulse-API.git
cd AgentPulse-API
# create a .env file (see below)
docker-compose up --build
```

API at `http://localhost:8000` · interactive docs (Swagger) at `http://localhost:8000/docs`

`.env` example:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=agent_pulse_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/agent_pulse_db
```

## Tests

```bash
python -m pytest
```

17 tests covering the API endpoints, Celery configuration, database, schemas and deterministic tools, the repair loop (success on 1st attempt, success after repair, exhaustion) and worker–orchestrator integration.

## Known limitations

- **No real LLM is wired by default.** The orchestrator accepts any LLM as a plain function (`prompt -> str`); without one, it uses a built-in stub that returns valid JSON. Connecting a provider (OpenAI, Groq, a local model…) is a one-function change.
- The deterministic tool is a simple risk score over items with severity labels — a demonstration of keeping arithmetic out of the LLM, not a domain model.
- Throughput and scaling have not been benchmarked.

## Tech stack

Python 3.11 · FastAPI · Celery · Redis · PostgreSQL (SQLAlchemy async, Alembic) · Pydantic · tenacity · Docker Compose · pytest

## License

[MIT](LICENSE)
