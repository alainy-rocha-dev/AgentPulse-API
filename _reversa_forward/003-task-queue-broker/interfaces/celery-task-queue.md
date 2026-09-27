# Contrato de Fila: `celery-task-queue`

> Contrato de Mensageria da Fila de Tarefas Assíncronas  
> Tipo: Fila Celery / Redis  

---

## 1. Payload de Entrada da Tarefa (`celery_app.send_task`)

- **Nome da Tarefa:** `app.worker.execute_agent_task`
- **Argumentos (kwargs):**
  - `task_id` (str, UUID format): ID da tarefa registrada no PostgreSQL.
  - `payload` (dict): Conteúdo da requisição a ser processada pela inteligência dos agentes.

## 2. Configurações da Fila Celery

- **Fila Padrão:** `default`
- **Confirmação Tardia (`acks_late`):** `True`
- **Rejeição por Perda de Worker (`task_reject_on_worker_lost`):** `True`
- **Limite Estrito de Tempo (`task_time_limit`):** `300` segundos
- **Limite Suave de Tempo (`task_soft_time_limit`):** `280` segundos

## 3. Comportamento de Erro

- **Timeout:** Dispara `SoftTimeLimitExceeded` / `TimeLimitExceeded`, cancelando o worker e alterando o estado da tarefa para `failed`.
- **Desconexão com PostgreSQL:** Tenta reconectar até 3 vezes com backoff exponencial antes de lançar exceção.
