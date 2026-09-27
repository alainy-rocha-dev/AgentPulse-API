# Onboarding Executável: `task-queue-broker`

> Feature: `003-task-queue-broker`  
> Data: `2026-09-27`  

---

## Passo a Passo para Validação Manual da Fila Celery

1. **Iniciar Instância do Redis:**
   ```bash
   docker run -d --name redis-broker -p 6379:6379 redis:alpine
   ```

2. **Executar o Celery Worker:**
   ```bash
   celery -A app.core.celery_app.celery_app worker --loglevel=info
   ```

3. **Submeter uma Tarefa de Teste:**
   - Enviar uma requisição POST no endpoint `/api/v1/tasks` do API Gateway.
   - Observar nos logs do Celery Worker o consumo da mensagem e a alteração de status para `running`.

4. **Validar Suíte de Testes Automatizados:**
   ```bash
   pytest tests/test_task_queue_broker.py
   ```
