# Requirements: Persistência PostgreSQL e Orquestração Docker (`postgres-persistence-container`)

> Identificador: `004-postgres-persistence-container`  
> Data: `2026-09-27`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

O componente `postgres-persistence-container` é responsável por implementar a camada de persistência relacional permanente no PostgreSQL 16 e a orquestração completa em múltiplos containers via Docker Compose. Garante a integridade histórica dos dados das tarefas de IA (`tasks`), migrações assíncronas via Alembic e inicialização sequencial resiliente garantida por healthchecks.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#Escopo` | Persistência do histórico e resultado final no PostgreSQL; Containerização via Docker Compose. | 🟡 |
| `_reversa_sdd/sdd/postgres-persistence-container.md#RF-01` | Tabela `tasks` com colunas `id` (UUID), `status`, `payload`, `result`, `error` e timestamps. | 🟢 |
| `_reversa_sdd/sdd/postgres-persistence-container.md#RF-04` | Healthcheck para PostgreSQL e Redis garantindo subida ordenada do FastAPI e Celery. | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Engenheiro Backend | Subir toda a infraestrutura com um único comando `docker-compose up` | Execução em ambiente de dev/teste sem falhas de conexão de banco. |
| Desenvolvedor de IA | Garantir que o resultado das cadeias de agentes não se perca após reiniciar containers | Gravação persistente no volume PostgreSQL nomeado. |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** A tabela `tasks` deve possuir chave primária UUID e índices no campo `status` e `created_at` para otimização de consultas. 🟢
2. **RN-02:** O container da aplicação FastAPI e do Worker Celery só devem iniciar após a confirmação de que o PostgreSQL e Redis estão prontos e aceitando conexões (`service_healthy`). 🟢
3. **RN-03:** O volume de dados do PostgreSQL deve ser persistente entre reinicializações e destruições de containers. 🟢

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar modelagem SQLAlchemy e script de migração Alembic para a tabela `tasks` | Must | Tabela `tasks` gerada no banco PostgreSQL com schema especificado. | 🟢 |
| RF-02 | Criar e validar o `docker-compose.yml` orquestrando os serviços `web`, `worker`, `redis` e `db` | Must | Todos os 4 serviços iniciam e passam pelos testes de conectividade. | 🟢 |
| RF-03 | Configurar volume nomeado no Docker Compose para dados do PostgreSQL | Must | Dados inseridos em `tasks` persistem após `docker-compose down` e `docker-compose up`. | 🟢 |
| RF-04 | Incluir `healthcheck` com `pg_isready` para o serviço `db` e `redis-cli ping` para o `redis` | Must | Dependências iniciam sequencialmente sem falhas de conexão na startup. | 🟢 |
| RF-05 | Fornecer arquivo `.env.example` preenchido com todas as variáveis de ambiente necessárias | Should | Aplicação inicia sem erros de variáveis ausentes ao copiar para `.env`. | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Tempo de inicialização total da stack no Docker Compose inferior a 2 minutos | `_reversa_sdd/prd.md#Métricas` | 🟡 |
| Resiliência | Reconexão automática em caso de queda temporária do banco ou broker | Retries com `tenacity` e `asyncpg` / `psycopg2` | 🟢 |
| Segurança | Variáveis sensíveis e senhas do banco de dados isoladas no `.env` e descartadas do repositório | `.gitignore` e `.env.example` | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Subida completa dos containers em ambiente limpo
  Dado que o usuário executa "docker-compose up --build"
  Quando os healthchecks dos serviços "db" e "redis" retornarem status healthy
  Então os serviços "web" e "worker" iniciam a execução e conectam-se ao PostgreSQL sem erros.

Cenário: Persistência de dados após reinício da stack
  Dado que um registro de tarefa existe no PostgreSQL
  Quando a stack Docker for interrompida com "docker-compose down" e reiniciada com "docker-compose up"
  Então o registro na tabela "tasks" continua acessível via API GET /tasks/{task_id}.
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Modelo + Migração Alembic) | Must | Estrutura de dados essencial para todas as features. |
| RF-02 (docker-compose.yml 4 serviços) | Must | Requisito central de infraestrutura do PRD. |
| RF-03 (Volume PostgreSQL) | Must | Garantia contra perda de dados históricos. |
| RF-04 (Healthchecks) | Must | Previne Condição de Corrida (Race Condition) na inicialização dos containers. |
| RF-05 (.env.example) | Should | Boas práticas de reprodutibilidade de ambiente. |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

- Nenhuma lacuna ou dúvida registrada. O escopo e especificações técnica estão completamente definidos em `_reversa_sdd/sdd/postgres-persistence-container.md`.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-requirements` | reversa-requirements |
