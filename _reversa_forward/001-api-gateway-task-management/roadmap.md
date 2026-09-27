# Roadmap: API Gateway & Gerenciamento de Tarefas Assíncronas

> Identificador: `001-api-gateway-task-management`  
> Data: `2026-09-27`  
> Requirements: `_reversa_forward/001-api-gateway-task-management/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

A arquitetura do API Gateway para a feature 001 baseia-se em FastAPI para servir requisições HTTP de alta performance. Ao receber `POST /tasks`, um middleware inspeciona o `Content-Length` (máximo 10 MB). Os dados são validados pelo schema Pydantic `TaskCreate`. Um UUIDv4 é gerado e registrado no banco PostgreSQL com status `queued`. Em seguida, a tarefa é publicada no broker Redis utilizando Celery Client. A API retorna imediatamente HTTP 202 Accepted contendo o `task_id`. O endpoint `GET /tasks/{task_id}` faz a leitura do status e resultado diretamente do banco de dados/Redis.

---

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| n/a | Nenhum arquivo `principles.md` definido | n/a |

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | FastAPI como web framework | Performance assíncrona com `asyncio`, OpenAPI automático | Flask, Django REST Framework | 🟢 |
| D-02 | Pydantic v2 para validação | Alta velocidade (C++ core), sintaxe limpa, suporte a tipos estritos | Cerberus, Marshmallow | 🟢 |
| D-03 | Celery + Redis para enfileiramento | Padrão robusto para ecossistema Python com suporte nativo a retries e distribuição de workers | RabbitMQ, RQ, Kafka | 🟢 |
| D-04 | PostgreSQL + SQLAlchemy | Persistência relacional de histórico de execuções de tarefas de IA | MongoDB, SQLite | 🟢 |
| D-05 | Middleware de limite 10 MB | Prevenção contra exaustão de memória no servidor web | Limitar apenas na camada de proxies/Nginx | 🟢 |

---

## 4. Premissas

> Nenhuma premissa pendente. Todas as dúvidas do `requirements.md` foram esclarecidas.

---

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `app/api/v1/endpoints/tasks.py` | `_reversa_sdd/sdd/api-gateway-task-management.md` | componente-novo | Controladores REST para submissão e polling de tarefas |
| `app/schemas/task.py` | `_reversa_sdd/sdd/api-gateway-task-management.md` | componente-novo | Schemas Pydantic `TaskCreate`, `TaskResponse`, `TaskStatus` |
| `app/models/task.py` | `_reversa_sdd/sdd/postgres-persistence-container.md` | componente-novo | Modelo ORM SQLAlchemy para tabela `tasks` |
| `app/core/celery_app.py` | `_reversa_sdd/sdd/task-queue-broker.md` | componente-novo | Configuração e inicialização do cliente Celery |

---

## 6. Delta no modelo de dados

- Criada a tabela `tasks` no PostgreSQL contendo identificador UUID `id`, payload de entrada, tipo da tarefa, status (`queued`, `processing`, `completed`, `failed`), resultado em JSONB e timestamps.
- Detalhe completo em: `_reversa_forward/001-api-gateway-task-management/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| HTTP Tasks API (`/tasks`) | HTTP | `_reversa_forward/001-api-gateway-task-management/interfaces/http-tasks-api.md` |

---

## 8. Plano de migração

1. Criar migration inicial no Alembic (`alembic revision --autogenerate -m "create_tasks_table"`).
2. Executar upgrade na base PostgreSQL (`alembic upgrade head`).
3. Verificar conectividade da API com o Redis Broker e PostgreSQL na inicialização da stack Docker.

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Queda do serviço Redis | Alto | Baixa | Retries com reconexão automática e log estruturado |
| Envio de arquivo gigante | Médio | Média | Middleware validando `Content-Length` até 10 MB com HTTP 413 |
| Concorrência de polling em alto volume | Médio | Média | Leitura indexada por `task_id` (PK UUID) no PostgreSQL |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Endpoints `POST /tasks` e `GET /tasks/{task_id}` testados e operacionais
- [ ] Tabela `tasks` criada via Alembic no PostgreSQL
- [ ] Docker Compose inicializando API, Redis e Postgres com sucesso

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-plan` | reversa |
