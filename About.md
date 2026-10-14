# About

**AgentPulse API** — Async AI Agent Orchestration Engine

Uma API assíncrona de alta performance construída com FastAPI, Celery e PostgreSQL, projetada para orquestrar agentes de IA com processamento desacoplado, repair loop anti-alucinação e fila Celery/Redis. Ideal para aplicações que exigem execução longa sem timeouts HTTP.

**Características principais:**
- Processamento assíncrono desacoplado via Celery + Redis
- Validação determinística com Repair Loop Pydantic
- Persistência confiável em PostgreSQL
- Containerização Docker 100% reprodutível
- Cobertura total de testes automatizados

**Tecnologias:** Python 3.11+, FastAPI, Celery, SQLAlchemy, Pydantic, Redis, PostgreSQL

**Endpoints:** POST /tasks, GET /tasks/{id}