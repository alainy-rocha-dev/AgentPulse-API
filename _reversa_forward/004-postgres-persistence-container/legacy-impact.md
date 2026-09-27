# Impacto no Legado: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  
> Política de edição: `allowLegacyEdits: true` (liberação irrestrita)  
> Nota de Âncora: Feature greenfield, sem legado pré-existente. Âncora: `prd.md` + specs SDD em `_reversa_sdd/sdd/postgres-persistence-container.md`.  

## Tabela de Impactos por Arquivo

| Arquivo afetado | Componente SDD | Tipo | Severidade | Justificativa |
|-----------------|----------------|------|------------|---------------|
| `app/core/config.py` | `postgres-persistence-container` | `componente-novo` | LOW | Adição de configurações de conexão síncronas e assíncronas ao PostgreSQL |
| `app/core/database.py` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Configuração do AsyncEngine SQLAlchemy, AsyncSessionLocal e Base |
| `app/models/task.py` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Definição da classe ORM Task com campos UUID, JSONB e timestamps |
| `alembic/env.py` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Configuração de migrações assíncronas e síncronas com Alembic |
| `alembic/versions/001_create_tasks_table.py` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Script de migração DDL inicial para a tabela tasks e seus índices |
| `docker-compose.yml` | `postgres-persistence-container` | `componente-novo` | HIGH | Orquestração multi-container com serviço db (PostgreSQL 16) e volume persistente postgres_data |
| `Dockerfile` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Configuração do entrypoint para automação de migrações |
| `entrypoint.sh` | `postgres-persistence-container` | `componente-novo` | MEDIUM | Script de inicialização dos containers executando alembic upgrade head |
| `tests/test_database.py` | `postgres-persistence-container` | `componente-novo` | LOW | Testes unitários para modelo ORM Task e URLs de conexão |

## Diff Conceitual por Componente

### Componente `postgres-persistence-container`
Em modo greenfield, o componente foi construído segundo as especificações em `_reversa_sdd/sdd/postgres-persistence-container.md`. Foram criadas as definições ORM SQLAlchemy, suporte a migrações Alembic e containerização via Docker Compose com volume persistente `postgres_data`.

## Regras Preservadas

_Sem regras preservadas de legado (projeto greenfield)._

## Regras Modificadas

_Sem regras modificadas de legado (projeto greenfield)._
