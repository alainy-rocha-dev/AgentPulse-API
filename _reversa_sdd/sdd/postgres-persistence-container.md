# Spec SDD: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Selo 🟡 PLANEJADO. Especificação técnica de componente gerada por reversa-spec-sdd.

**Versão:** 1.0  
**Data:** 2026-09-27T11:38:47-03:00  
**Componente:** `postgres-persistence-container`  
**Status:** Aprovado  

---

## 1. Visão Geral e Problema

🟡 O componente `postgres-persistence-container` gerencia a camada de armazenamento relacional permanente no PostgreSQL e a containerização multi-serviços via Docker Compose. Ele garante que a API, Redis, Celery Workers e PostgreSQL subam perfeitamente com um único comando (`docker-compose up`) e mantenham a integridade dos dados históricos de tarefas.

---

## 2. Requisitos Funcionais (RF)

| ID | Descrição do Requisito | Selo |
|---|---|---|
| **RF-01** | O modelo de dados em PostgreSQL deve conter a tabela `tasks` com as colunas: `id` (UUID), `status` (string), `payload` (JSONB), `result` (JSONB), `error` (text), `created_at` (timestamp) e `updated_at` (timestamp). | 🟡 |
| **RF-02** | O arquivo `docker-compose.yml` deve definir e orquestrar 4 serviços isolados: `web` (FastAPI), `redis` (Broker), `worker` (Celery) e `db` (PostgreSQL 16). | 🟡 |
| **RF-03** | O serviço `db` deve possuir um volume persistente do Docker configurado para garantir a permanência dos dados após a reinicialização dos containers. | 🟡 |
| **RF-04** | O `docker-compose.yml` deve incluir `healthcheck` para os serviços de banco e redis, garantindo que os containers `web` e `worker` só iniciem após o banco estar pronto (`depends_on` com `condition: service_healthy`). | 🟡 |
| **RF-05** | O repositório deve fornecer um arquivo `.env.example` completo com todas as variáveis de ambiente necessárias para a execução do container. | 🟡 |

---

## 3. Escopo e Limites do Componente

### O que está DENTRO (In)
- 🟡 Modelagem SQLAlchemy / SQLModel da tabela de tarefas
- 🟡 Script de migração de banco (Alembic) ou inicialização de tabelas
- 🟡 Arquivo `docker-compose.yml` com healthchecks e volumes
- 🟡 Arquivo `.env.example` e `Dockerfile` multi-stage

### O que está FORA (Out)
- 🟡 Deploy automatizado em Kubernetes ou ambientes Serverless de nuvem

---

## 4. Edge Cases e Tratamento de Erros

- 🟡 **Edge Case 1 (Tentativa de subida de containers antes do banco estar pronto):** Resolvido via Docker Healthchecks no PostgreSQL (`pg_isready`).
- 🟡 **Edge Case 2 (Dados nulos ou JSON corrompido no resultado):** Campo `result` definido como `JSONB` anulável, populado somente quando o status for `"completed"`.
- 🟡 **Edge Case 3 (Concorrência na atualização de status):** Locks otimistas ou transações isoladas em SQLAlchemy.

---

## 5. Critérios de Aceite (Dado / Quando / Então)

- 🟡 **Dado** um ambiente zerado com Docker instalado, **Quando** o comando `docker-compose up --build` é executado, **Então** os 4 containers sobem e ficam saudáveis em < 2 minutos.
- 🟡 **Dado** que uma tarefa é finalizada pelo worker, **Quando** o resultado é gravado, **Então** o registro na tabela `tasks` em PostgreSQL é atualizado atomicamente com status `"completed"`.

---

## 6. Avaliação de Qualidade (Score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
SCORE TOTAL: 90/100  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

Breakdown:  
  Completude:    92/100 (peso 30%)  
  Testabilidade: 90/100 (peso 25%)  
  Clareza:       90/100 (peso 20%)  
  Escopo:        88/100 (peso 15%)  
  Edge Cases:    88/100 (peso 10%)  

Gaps críticos: Nenhum.  
Sugestões: Incluir comandos de rotina de backup no README.

---
Gerado por reversa-spec-sdd em 2026-09-27T11:38:47-03:00
