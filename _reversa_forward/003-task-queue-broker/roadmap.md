# Roadmap: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Identificador: `003-task-queue-broker`
> Data: `2026-09-27`
> Requirements: `_reversa_forward/003-task-queue-broker/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

---

## 1. Resumo da abordagem

A abordagem para o `task-queue-broker` estabelece a infraestrutura de mensageria assíncrona com Redis Broker e Celery Workers. A integração conecta a criação de tarefas no API Gateway (FastAPI) aos trabalhadores assíncronos, configurando o broker com confirmação tardia (`acks_late=True`), tempo limite por tarefa (`task_time_limit=300s`), e atualização síncrona do estado das tarefas no PostgreSQL (`running`, `completed`, `failed`).

---

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Resiliência e Tolerância a Falhas | Celery configurado com `acks_late` e `task_time_limit` garante recuperação automática | Respeita |
| Rastreabilidade de Estado | Transições explícitas de estado (`pending` -> `running` -> `completed`/`failed`) no DB | Respeita |

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Utilizar Celery com Redis como Broker de Mensageria | Solução padrão da indústria para mensageria Python robusta e distribuída | RabbitMQ (mais complexo), ARQ (menos maduro) | 🟢 |
| D-02 | Habilitar `acks_late=True` e `task_reject_on_worker_lost=True` | Garante que mensagens sejam reenfileiradas se o worker sofrer crash | Standard ACK no início da tarefa | 🟢 |
| D-03 | Configurar `task_time_limit=300` | Previne tarefas travadas indefinidamente por timeouts em chamadas LLM | Sem timeout (risco de leilão de conexões) | 🟢 |
| D-04 | Atualização transacional de estado no PostgreSQL ao consumir tarefa | Garante que o cliente veja estado `running` instantaneamente | Polling no Redis | 🟡 |

---

## 4. Premissas

> Nenhuma premissa sob dúvida.

---

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `task-queue-broker` | `_reversa_sdd/sdd/task-queue-broker.md` | componente-novo | Módulo `app/core/celery_app.py` configurando o Celery com Redis |
| `task-worker` | `_reversa_sdd/sdd/task-queue-broker.md` | regra-alterada | Módulo `app/worker.py` interceptando eventos do ciclo de vida das tarefas |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma alteração estrutural nas tabelas; atualização nos valores do enum/campo `status` da tabela de tarefas (`pending`, `running`, `completed`, `failed`).
- Detalhe completo em: `_reversa_forward/003-task-queue-broker/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Celery Task Queue | fila | `_reversa_forward/003-task-queue-broker/interfaces/celery-task-queue.md` |

---

## 8. Plano de migração

1. n/a (Infraestrutura inicial do broker e workers Celery).

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Acúmulo de mensagens não consumidas no Redis | médio | baixo | Monitoramento de filas Celery e timeout estrito de 300s |
| Desconexão com o PostgreSQL ao atualizar status | médio | baixo | Retentativas exponenciais de reconexão via decorador Tenacity no worker |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Suíte de testes unitários e de integração de mensageria passando
- [ ] `regression-watch.md` gerado

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-plan` | reversa-plan |
