# Actions: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Identificador: `003-task-queue-broker`  
> Data: `2026-09-27`  
> Roadmap: `_reversa_forward/003-task-queue-broker/roadmap.md`  

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 7 |
| Paralelizáveis (`[//]`) | 3 |
| Maior cadeia de dependência | 4 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Criar/configurar o módulo Celery App (`app/core/celery_app.py`) com Redis, `acks_late=True` e `task_time_limit=300` | - | `[//]` | `app/core/celery_app.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T002 | Criar suíte de testes unitários para a configuração do Celery e parâmetros de resiliência em `tests/test_celery_config.py` | T001 | `[//]` | `tests/test_celery_config.py` | 🟢 | `[X]` |
| T003 | Criar suíte de testes de integração para o consumo de mensagens da fila Celery em `tests/test_task_queue_broker.py` | T001 | `[//]` | `tests/test_task_queue_broker.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T004 | Atualizar a gestão do ciclo de vida das tarefas no Celery worker (`app/worker.py`) garantindo a transição para `running` ao consumir | T001 | - | `app/worker.py` | 🟢 | `[X]` |
| T005 | Implementar retentativas exponenciais (`tenacity`) para atualizações do PostgreSQL no Celery worker | T004 | - | `app/worker.py` | 🟡 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T006 | Garantir que os endpoints da API registrem e publiquem as tarefas no broker Celery | T001 | - | `app/services/task_service.py` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Adicionar logging detalhado e métricas de consumo de mensagens no Celery Worker | T005 | - | `app/worker.py` | 🟢 | `[X]` |

## Notas de execução

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-to-do` | reversa-to-do |
