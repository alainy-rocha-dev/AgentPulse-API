# Investigação Técnica: API Gateway & Gerenciamento de Tarefas Assíncronas

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  

---

## 1. Padrões de Arquitetura Investigados

### Asynchronous Request-Reply Pattern (Enterprise Integration Pattern)
- **Problema:** Requisições HTTP síncronas para chamadas de LLM causam timeout no cliente (muitas vezes levando mais de 30 segundos para responder).
- **Solução:** O API Gateway responde de imediato HTTP 202 Accepted com um identificador de recurso (`task_id`) e um cabeçalho/body apontando para a URI de polling (`GET /tasks/{task_id}`).
- **Padrão de enfileiramento:** Utilização do Celery com Redis como message broker garante que o recebimento da mensagem seja rápido e resiliente.

---

## 2. Frameworks e Bibliotecas Escolhidas

1. **FastAPI (>= 0.110.0):** Escolhido por suporte nativo a operações `async/await`, excelente performance com uvicorn e geração automática da documentação Swagger/OpenAPI.
2. **Pydantic v2:** Fornece rápida validação de tipos e schemas Python via Rust core.
3. **Celery (>= 5.3.0):** Sistema de fila de tarefas distribuídas maduro no ecossistema Python.
4. **SQLAlchemy v2 / SQLModel:** ORM moderno com suporte assíncrono para PostgreSQL.

---

## 3. Fontes de Referência
- [FastAPI Async Documentation](https://fastapi.tiangolo.com/async/)
- [Celery First Steps with Redis](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#redis)
- [Microsoft REST API Guidelines - Async Operations](https://github.com/microsoft/api-guidelines)
