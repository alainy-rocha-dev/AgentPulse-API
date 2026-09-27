# Pesquisa e Investigação Técnica: `task-queue-broker`

> Feature: `003-task-queue-broker`  
> Data: `2026-09-27`  

---

## 1. Padrões de Mensageria e Arquitetura de Fila

Para garantia de processamento assíncrono resiliente de tarefas de agentes de IA, investigou-se as seguintes abordagens:

1. **Celery com Redis (Escolhido):**
   - **Vantagens:** Suporte maduro em Python, suporte nativo a `task_time_limit`, retries automáticos, `acks_late` e ecossistema robusto.
   - **Configurações recomendadas:**
     - `task_acks_late = True`: confirmação só após conclusão da tarefa.
     - `task_reject_on_worker_lost = True`: reenfileiramento automático se o worker sofrer crash.
     - `task_time_limit = 300`: hard limit de 300s para evitar bloqueio de workers por tarefas de LLM penduradas.
     - `result_backend = None`: os resultados são persistidos diretamente no PostgreSQL via ORM/SQLAlchemy.

2. **ARQ (Asyncio Redis Queue):**
   - Descartado devido à menor compatibilidade com tarefas síncronas bloqueantes e menor madurez de ferramentas de inspeção.

---

## 2. Tratamento de Exceções e Conectividade no Worker

- **Falhas de Conexão no Banco de Dados:** Utilização de retentativas exponenciais com o pacote `tenacity` durante as atualizações de estado do PostgreSQL.
- **Isolamento de Tarefas:** Cada tarefa é executada em isolamento pelo worker, garantindo sanitização do erro em bloco `try/except Exception` para gravação do campo `error_message`.
