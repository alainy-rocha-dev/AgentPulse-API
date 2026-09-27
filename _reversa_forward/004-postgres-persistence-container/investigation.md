# Investigation: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

## Pesquisa de Fundo e Contexto

A containerização multi-serviços com FastAPI, Celery, Redis e PostgreSQL exige controle estrito da ordem de inicialização. O uso de `depends_on` simples no Docker Compose não aguarda a prontidão real do banco PostgreSQL (apenas a inicialização do container). Portanto, a implementação de `healthcheck` nativo com `pg_isready` é o padrão da indústria para essa arquitetura.

## Alternativas Avaliadas

1. **Alembic vs SQLAlchemy `create_all`**: Alembic foi escolhido por permitir controle formal de versões de migração do banco relacional em produção.
2. **PostgreSQL 16 Alpine**: Imagem leve e oficial para Docker Compose.
