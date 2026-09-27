# Contrato de Interface: Celery Worker & Agent Orchestrator

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  
> Tipo: Fila Assíncrona (Celery / Redis)  

---

## 1. Entrada: Payload da Tarefa Celery

O worker Celery (`app/worker.py`) consome tarefas publicadas no Redis com o seguinte formato de argumentos:

```python
process_task.delay(task_id="550e8400-e29b-41d4-a716-446655440000", input_data={"prompt": "Analisar minuta contratual X", "parameters": {}})
```

### Campos:
- `task_id` (str, UUID): Identificador único da tarefa no PostgreSQL.
- `input_data` (dict): Conteúdo bruto para processamento pelos agentes de IA.

---

## 2. Saída Validada (Pydantic Schema: `AnalysisOutputSchema`)

```json
{
  "summary": "String descrevendo o resumo da análise",
  "key_findings": ["string"],
  "metrics": {
    "total_score": 0.0,
    "risk_level": "LOW | MEDIUM | HIGH",
    "calculated_items": 0
  },
  "metadata": {
    "repair_attempts": 0,
    "execution_time_seconds": 0.0,
    "model_used": "string"
  }
}
```

---

## 3. Idempotência e Retries de Fila
- Caso o Celery reinicie a tarefa por crash de processo, o `AgentOrchestrator` verifica o status atual da tarefa no PostgreSQL. Se já estiver `completed`, encerra imediatamente sem gastar chamadas de LLM.
