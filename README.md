# ⚡ AgentPulse API

> **Asynchronous AI Agent Orchestration & Validation Engine**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3%2B-green.svg)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-5.0%2B-red.svg)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791.svg)](https://www.postgresql.org/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Ready-2496ED.svg)](https://www.docker.com/)

**AgentPulse API** é um motor assíncrono de alta performance projetado para executar cadeias de agentes autônomos de Inteligência Artificial (ex: análise de contratos complexos, automação de marketing e processamento multimodal). 

A plataforma resolve o desafio de **timeouts HTTP em tarefas de longa duração** ao retornar uma resposta imediata (`202 Accepted`) com monitoramento de status, desacoplando o processamento pesado via **Celery + Redis** e garantindo determinismo em saídas de LLMs através de um **Repair Loop com Pydantic**.

---

## 🏛️ Arquitetura da Solução

```mermaid
flowchart TD
    Client([Cliente / Frontend]) -->|1. POST /api/v1/tasks| API[FastAPI Gateway]
    API -->|2. Retorna 202 Accepted + task_id| Client
    API -->|3. Enfileira Tarefa| Redis[(Redis Broker)]
    
    subgraph Background Processing
        Redis -->|4. Consome Fila| Worker[Worker Celery]
        Worker -->|5. Executa Agente IA| AgentEngine[Agent Orchestrator]
        AgentEngine -->|6. Valida Schema / Repair Loop| PydanticValidator[Pydantic Schema Validator]
    end
    
    Worker -->|7. Persiste Estado & Resultado| Postgres[(PostgreSQL DB)]
    Client -.->|"8. GET /api/v1/tasks/{task_id}"| API
    API -.->|9. Consulta Resultado| Postgres
```

---

## ✨ Principais Funcionalidades

- **⚡ Processamento Assíncrono Desacoplado**: Resposta HTTP imediata (`202 Accepted`) eliminando risco de timeout em conexões de longa duração.
- **🔄 Auto-Recuperação Anti-Alucinação (Repair Loop)**: Loop de retentativas inteligentes para corrigir JSONs mal-formados ou não-conformes gerados por LLMs.
- **📦 Fila Concorrente de Altura Escala**: Gerenciamento de tarefas em segundo plano impulsionado por **Celery** e **Redis**.
- **💾 Persistência Confiável**: Histórico completo de execução e payload de resultados armazenados em **PostgreSQL**.
- **🐳 Containerização 100% Reprodutível**: Toda a stack pronta para execução via **Docker Compose**.
- **🧪 Cobertura Total de Testes**: Suíte de testes automatizados integrando API, Workers, Banco de Dados e validações com **Pytest**.

---

## 🚀 Como Executar

### Pré-requisitos
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11+ (opcional para desenvolvimento local)

### 1. Clonar o Repositório
```bash
git clone https://github.com/alainy-rocha-dev/AgentPulse-API.git
cd AgentPulse-API
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` baseado nas configurações padrão:
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

### 3. Subir a Stack via Docker Compose
```bash
docker-compose up --build
```
A API estará acessível em: `http://localhost:8000`  
Documentação Interativa (Swagger/OpenAPI): `http://localhost:8000/docs`

---

## 🧪 Executando os Testes

Para executar a suíte completa de testes unitários e de integração:

```bash
python -m pytest
```

---

## 📌 Referência da API (Endpoints)

| Método | Endpoint | Descrição | Status Code |
|---|---|---|---|
| `POST` | `/api/v1/tasks` | Submete uma nova tarefa para execução assíncrona | `202 Accepted` |
| `GET` | `/api/v1/tasks/{task_id}` | Consulta o status e o resultado final da tarefa | `200 OK` |
| `GET` | `/health` | Verificação de integridade dos serviços | `200 OK` |

---

## 🛡️ Licença

Este projeto está sob a licença [MIT](LICENSE).
