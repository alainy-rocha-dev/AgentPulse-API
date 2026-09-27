# Requirements: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Identificador: `003-task-queue-broker`
> Data: `2026-09-27`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

---

## 1. Resumo executivo

O componente `task-queue-broker` gerencia a infraestrutura de mensageria assíncrona baseada em Redis e Celery. Ele é responsável por transportar com segurança as tarefas criadas pelo API Gateway até os Workers Celery, garantindo alta concorrência, retentativas exponenciais, limite de tempo de execução (`task_time_limit`), confirmação tardia (`acks_late`) e transições de estado confiáveis no PostgreSQL.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4-escopo-in` | Fila de tarefas assíncronas com Redis e Celery | 🟡 |
| `_reversa_sdd/sdd/task-queue-broker.md` | Especificação técnica completa do broker de mensageria e resiliência de trabalhadores | 🟡 |
| `_reversa_sdd/addenda/001-api-gateway-task-management.md` | API Gateway publica tarefas no Redis e inicializa registros no PostgreSQL | 🟢 |
| `_reversa_sdd/addenda/002-ai-agent-orchestrator-validator.md` | Workers consome tarefas e salvam resultado validado no banco | 🟢 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Engenheiro Backend | Processar tarefas assíncronas de longa duração de forma escalável | A API aceita a requisição, envia o job para o Redis, o Celery Worker consome e executa o processamento com isolamento e resiliência |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01 (Persistência do Broker):** O Redis deve rodar com persistência ativada (RDB/AOF) para evitar perda de mensagens enfileiradas em caso de reinício do serviço. 🟡
2. **RN-02 (Transição de Estado em Consumo):** Quando o Celery Worker inicia a execução de uma tarefa, o estado no banco de dados deve mudar imediatamente de `pending` para `running`. 🟢
3. **RN-03 (Timeout Limite de Execução):** O limite máximo de execução de uma tarefa por um Worker Celery deve ser de 300 segundos (`task_time_limit=300`). Excedido o tempo, a tarefa é interrompida. 🟢
4. **RN-04 (Ack Tardia - acks_late):** O Celery deve utilizar `acks_late=True` para que o envio de confirmação só ocorra após a conclusão, garantindo o reprocessamento se o worker sofrer crash durante o processamento. 🟡
5. **RN-05 (Tratamento de Falhas):** Se uma tarefa falhar de forma irrecuperável ou estourar o timeout, seu estado deve ser atualizado no PostgreSQL para `failed` com mensagem sanitizada. 🟢

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Configuração do Redis Broker e Celery App (`app/core/celery_app.py`) | Must | Instância Celery configurada conectando ao Redis via URL de ambiente | 🟡 |
| RF-02 | Configuração de resiliência e timeouts no Celery (`acks_late`, `task_time_limit=300`) | Must | Tarefas abortadas ao atingir 300s e reenfileiradas em crash | 🟡 |
| RF-03 | Gestão de ciclo de vida da tarefa no Worker (`app/worker.py`) | Must | Atualização no PostgreSQL para `running` ao iniciar e `completed`/`failed` ao terminar | 🟢 |
| RF-04 | Retentativa exponencial em falhas temporárias de banco de dados | Should | Worker tenta reconectar ao PostgreSQL antes de falhar o job | 🟡 |
| RF-05 | Monitoramento da fila de tarefas e estatísticas do Celery | Should | Suporte a inspeção do estado da fila e trabalhadores via CLI/código | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Latência de consumo de tarefas < 100ms em sistema ocioso | Comunicação Redis / Celery via conexões de socket de alto desempenho | 🟡 |
| Confiabilidade | 0 perda de tarefas por crash de Worker ou timeout de LLM | Mecanismos `acks_late`, RDB/AOF no Redis e `task_time_limit` | 🟢 |
| Resiliência | Recuperação automática pós-desconexão temporária com PostgreSQL | Retentativas exponenciais com decoradores Tenacity | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Processamento assíncrono bem-sucedido via Celery Worker
  Dado que uma tarefa é enviada para a fila Redis
  Quando um Celery Worker consome o evento
  Então o status da tarefa é alterado para "running"
  E ao concluir o processamento o status muda para "completed"

Cenário: Excedido o tempo limite de execução (Timeout)
  Dado que uma tarefa está em execução há 300 segundos
  Quando o task_time_limit é atingido
  Então o Celery cancela a execução do Worker
  E o status da tarefa no PostgreSQL é atualizado para "failed" com erro de timeout

Cenário: Crash do Worker antes de emitir ACK
  Dado que o Worker sofre um desligamento abrupto durante a execução
  Quando o Redis detecta a desconexão sem recebimento de ACK (acks_late=True)
  Então a mensagem retorna para a fila para ser consumida por outro Worker
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Celery App & Redis) | Must | Requisito básico de infraestrutura de mensageria |
| RF-02 (Resiliência & Timeouts) | Must | Previne tarefas presas infinitamente em execução |
| RF-03 (Gestão de Ciclo de Vida) | Must | Sincroniza estado da tarefa entre broker e banco |
| RF-04 (Retry em Desconexão DB) | Should | Evita falhas desnecessárias por flutuações de rede |
| RF-05 (Monitoramento da Fila) | Should | Auxilia operabilidade e debug do ambiente |

---

## 9. Esclarecimentos

> Nenhuma dúvida aberta nesta sessão.

---

## 10. Lacunas

> Nenhuma lacuna pendente.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-requirements` | reversa-requirements |
