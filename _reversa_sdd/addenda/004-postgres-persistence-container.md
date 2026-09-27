# Adendo da Feature 004 (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  
> Cenário: `greenfield`

## Vigência

Vigente desde 2026-09-27.

## Resumo da entrega

Configuração completa da camada de persistência relacional com PostgreSQL (SQLAlchemy + Alembic) e infraestrutura containerizada multi-serviços via Docker Compose (`api`, `worker`, `db`, `redis`). A stack conta com suporte a volumes nomeados persistentes (`postgres_data`), controle de versão de schema com migrações assíncronas/síncronas no startup (`entrypoint.sh`) e verificação de saúde com `pg_isready` e `redis-cli ping`. Foram concluídas 10 de 10 ações planejadas.

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/prd.md` | Persistência & Docker | `componente-novo` | Suporte a banco de dados relacional PostgreSQL 16 e Docker Compose multi-serviços configurado. |
| `_reversa_sdd/sdd/postgres-persistence-container.md` | Especificações | `componente-novo` | Mapeamento ORM SQLAlchemy da tabela `tasks` com migrações via Alembic e volume nomeado `postgres_data`. |
| `app/core/config.py` | Configuração | `componente-novo` | Configurações de conexões síncronas (`SYNC_DATABASE_URL`) e assíncronas (`ASYNC_DATABASE_URL`). |
| `app/core/database.py` | Sessão DB | `componente-novo` | Instanciação de AsyncEngine, AsyncSessionLocal e Base do SQLAlchemy. |
| `app/models/task.py` | Modelo ORM | `componente-novo` | Modelo ORM `Task` com colunas UUID, JSONB e timestamps. |
| `alembic/` | Migrações DDL | `componente-novo` | Estrutura Alembic configurada com script de migração inicial `001_create_tasks_table.py`. |
| `docker-compose.yml` | Containerização | `componente-novo` | Orquestração com serviço `db` (PostgreSQL 16), healthcheck `pg_isready` e volume `postgres_data`. |
| `Dockerfile` & `entrypoint.sh` | Build & Startup | `componente-novo` | Entrypoint configurado para automação de migrações (`alembic upgrade head`) antes de iniciar os serviços. |
| `tests/test_database.py` | Suíte de Testes | `componente-novo` | Testes unitários para validação das URLs de conexão e modelo ORM `Task`. |

## Regras sob vigilância

- Consultar observações e watch items na spec: `_reversa_forward/004-postgres-persistence-container/regression-watch.md`

## Fontes

- `_reversa_forward/004-postgres-persistence-container/legacy-impact.md`
- `_reversa_forward/004-postgres-persistence-container/requirements.md`
- `_reversa_forward/004-postgres-persistence-container/actions.md`
- `_reversa_forward/004-postgres-persistence-container/progress.jsonl`
