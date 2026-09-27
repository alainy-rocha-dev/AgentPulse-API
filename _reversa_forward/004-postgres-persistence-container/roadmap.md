# Roadmap: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  
> Requirements: `_reversa_forward/004-postgres-persistence-container/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

Configuração da persistência relacional do banco PostgreSQL usando SQLAlchemy e migrações assíncronas/síncronas com Alembic, aliada à orquestração containerizada multi-serviço via Docker Compose. Serão definidos os serviços `web` (FastAPI), `worker` (Celery), `redis` (Broker) e `db` (PostgreSQL 16), com healthchecks garantindo inicialização limpa e volumes nomeados para garantia da permanência dos dados.

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Infraestrutura Reprodutível | Orquestração centralizada via Docker Compose com suporte a `.env`. | respeita |
| Resiliência de Dados | Volumes persistentes e migrações estruturadas via Alembic. | respeita |

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Utilizar Alembic para migrações do PostgreSQL | Controle de versão de schema e suporte a updates evolutivos. | `SQLAlchemy.metadata.create_all()` direto | 🟢 |
| D-02 | Configurar Docker Healthchecks com `pg_isready` e `redis-cli ping` | Evita falhas de inicialização nos containers dependentes (`web` e `worker`). | Retries genéricos com tempo fixo (`sleep`) | 🟢 |
| D-03 | Usar volume nomeado Docker `postgres_data` | Garante que os dados em `tasks` permaneçam preservados entre `docker-compose down/up`. | Bind mount local direto ou container efêmero | 🟢 |

## 4. Premissas

Nenhuma premissa adotada a partir de dúvidas, requisitos 100% confirmados pelas especificações do projeto.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| PostgreSQL Persistence | `_reversa_sdd/sdd/postgres-persistence-container.md` | componente-novo | Mapeamento ORM SQLAlchemy da tabela `tasks` e suporte a Alembic. |
| Docker Compose Multi-service | `_reversa_sdd/sdd/postgres-persistence-container.md` | componente-novo | Orquestração multi-container para `web`, `worker`, `redis` e `db`. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Adicionada definição ORM SQLAlchemy em `app/models/task.py` e scripts de migração Alembic para criação inicial da tabela `tasks`.
- Detalhe completo em: `_reversa_forward/004-postgres-persistence-container/data-delta.md`

## 7. Delta de contratos externos

Nenhum novo contrato externo adicionado nesta feature (infraestrutura e banco de dados).

## 8. Plano de migração

1. Criar o diretório de migrações `alembic/` e arquivo `alembic.ini`.
2. Gerar a primeira migração com a tabela `tasks`.
3. Adicionar comando de execução de migrações na inicialização do serviço `web` ou script de entrypoint.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Demora na subida do PostgreSQL travando containers | médio | baixa | `healthcheck` via `pg_isready` e `depends_on` com `condition: service_healthy`. |
| Perda de dados em acidentes de desenvolvimento | alto | baixa | Volume nomeado explícito no `docker-compose.yml`. |

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] `regression-watch.md` gerado
- [ ] Testes de subida dos containers executados e validados

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-plan` | reversa-plan |
