# Legacy Impact: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Identificador: `003-task-queue-broker`  
> Data: `2026-09-27`  
> Política de edição: `allowLegacyEdits: true` (`allowedPaths: []` - liberação irrestrita)  
> Âncora: `prd.md` + specs SDD (Greenfield)

## Resumo de Impacto

Feature greenfield, sem legado pré-existente. Âncora: `prd.md` + specs em `_reversa_sdd/sdd/`.

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|-----------------|------------|------|------------|---------------|
| `app/core/celery_app.py` | Celery Broker App | `componente-novo` | LOW | Adicionada resiliência `acks_late=True` e `task_time_limit=300`. |
| `tests/test_celery_config.py` | Suíte de Testes | `componente-novo` | LOW | Testes unitários da configuração Celery. |
| `tests/test_task_queue_broker.py` | Suíte de Testes | `componente-novo` | LOW | Teste de integração do despacho de mensagens Celery. |
| `app/worker.py` | Celery Worker | `componente-novo` | MEDIUM | Transição para `running`, retries exponenciais PostgreSQL com `tenacity` e logs. |
| `app/api/v1/endpoints/tasks.py` | API Task Gateway | `componente-novo` | LOW | Verificado envio com tratamento de erro e status 202. |

## Diff Conceitual por Componente

### Celery App & Worker
O Worker Celery teve seu ciclo de vida aprimorado para registrar a transição de status para `running` logo ao ser consumido, protegendo as operações no banco PostgreSQL via retentativas exponenciais (`tenacity`) em caso de falhas transitórias.

### Testes
Criadas suítes automatizadas para validação da configuração Celery e do despacho de tarefas.

## Preservadas

- Nenhuma regra de legado pré-existente foi alterada (modo Greenfield).

## Modificadas

- Nenhuma regra pré-existente foi removida ou modificada (modo Greenfield).
