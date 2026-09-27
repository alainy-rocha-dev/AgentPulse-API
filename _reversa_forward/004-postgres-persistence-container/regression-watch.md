# Regression Watch: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  

## Tabela de Verificação de Regressão

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|--------------------------|------------------------------|---------------------|-------------------|

## Observações

- **RF-004-1 (Mapeamento ORM):** A classe `Task` em `app/models/task.py` mapeia a tabela `tasks` com colunas UUID, JSONB e timestamps.
- **RF-004-2 (Migrações Alembic):** O diretório `alembic/` e a migração `001_create_tasks_table.py` garantem a evolução controlada do schema PostgreSQL.
- **RF-004-3 (Docker Multi-Container):** O serviço `db` no `docker-compose.yml` utiliza a imagem `postgres:16-alpine` com volume nomeado `postgres_data` e healthcheck `pg_isready`.

## Histórico de re-extrações

_Nenhuma re-extração executada até o momento._

## Arquivadas

_Nenhum item arquivado._
