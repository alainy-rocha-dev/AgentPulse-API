# Actions: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  
> Roadmap: `_reversa_forward/004-postgres-persistence-container/roadmap.md`  

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 10 |
| Paralelizáveis (`[//]`) | 3 |
| Maior cadeia de dependência | 6 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Atualizar configurações e variáveis de ambiente para conexão PostgreSQL | - | `[//]` | `app/core/config.py` | 🟢 | `[X]` |
| T002 | Adicionar dependências SQLAlchemy, asyncpg, psycopg2-binary e Alembic | - | `[//]` | `requirements.txt` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar testes unitários para verificação de sessão e conexão com o banco de dados | T001 | - | `tests/test_database.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Configurar engine, SessionLocal e Base do SQLAlchemy | T001, T002 | - | `app/core/database.py` | 🟢 | `[X]` |
| T005 | Definir modelo ORM SQLAlchemy para a entidade Task | T004 | - | `app/models/task.py` | 🟢 | `[X]` |
| T006 | Configurar env.py do Alembic com metadados do SQLAlchemy | T005 | - | `alembic/env.py` | 🟢 | `[X]` |
| T007 | Criar arquivo de migração inicial do Alembic para a tabela tasks | T006 | - | `alembic/versions/001_initial_tasks.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T008 | Atualizar docker-compose.yml com serviço db, healthcheck pg_isready e volume postgres_data | T001 | - | `docker-compose.yml` | 🟢 | `[X]` |
| T009 | Atualizar Dockerfile e entrypoint para executar alembic upgrade head na inicialização | T007, T008 | - | `Dockerfile` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T010 | Documentar comandos de migração e estrutura de persistência no onboarding | T009 | `[//]` | `_reversa_forward/004-postgres-persistence-container/onboarding.md` | 🟢 | `[X]` |

## Notas de execução

Todas as 10 ações foram concluídas e verificadas com sucesso. A suíte completa de 17 testes do pytest passou sem nenhuma falha.

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-to-do` | reversa-to-do |
| 2026-09-27 | Todas as tarefas T001 a T010 marcadas como [X] após implementação e testes passarem | reversa-coding |
