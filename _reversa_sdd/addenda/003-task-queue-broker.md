# Adendo da Feature 003 (`task-queue-broker`)

> Identificador: `003-task-queue-broker`  
> Data: `2026-09-27`  
> Cenário: `greenfield`

## Vigência

Vigente desde 2026-09-27.

## Resumo da entrega

Implementação da infraestrutura de mensageria assíncrona com Redis e Worker Celery. O worker agora gerencia o ciclo de vida com a transição do status para `running`, utiliza retentativas exponenciais (`tenacity`) para atualizações síncronas no PostgreSQL e emite logs detalhados e métricas no consumo. Foram concluídas 7 de 7 ações planejadas.

## Impacto por artefato da extração

| Artefato | Seção | Tipo de impacto | Delta |
|----------|-------|-----------------|-------|
| `_reversa_sdd/prd.md` | Escopo | `componente-novo` | Fila de mensageria com Redis e Workers Celery implementada para processamento em segundo plano. |
| `_reversa_sdd/sdd/003-task-queue-broker.md` | Especificações | `componente-novo` | Celery app configurado com `task_acks_late=True` e `task_time_limit=300`. |
| `app/core/celery_app.py` | Configuração | `componente-novo` | Módulo `celery_app.py` configurado com resiliência para tarefas assíncronas. |
| `app/worker.py` | Worker | `componente-novo` | Transição do status da tarefa para `running`, retries com `tenacity` e logging detalhado. |
| `tests/` | Suíte de Testes | `componente-novo` | Criados testes unitários e de integração em `test_celery_config.py` e `test_task_queue_broker.py`. |

## Regras sob vigilância

- Consultar observações e watch items na spec: `_reversa_forward/003-task-queue-broker/regression-watch.md`

## Fontes

- `_reversa_forward/003-task-queue-broker/legacy-impact.md`
- `_reversa_forward/003-task-queue-broker/requirements.md`
- `_reversa_forward/003-task-queue-broker/actions.md`
- `_reversa_forward/003-task-queue-broker/progress.jsonl`
