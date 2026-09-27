# Delta de Dados: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  

---

## 1. Visão Geral de Persistência

A Feature 002 utiliza a tabela `tasks` criada pela Feature 001 (`postgres-persistence-container`). Não são necessárias alterações de esquema no banco PostgreSQL (sem migrations novas do Alembic).

---

## 2. Estrutura do Payload JSON (Coluna `result` na Tabela `tasks`)

Quando a execução da cadeia de agentes é concluída com sucesso (status `completed`), a coluna `result` da tabela `tasks` armazena o JSON sanitizado e validado pelo Pydantic (`AnalysisOutputSchema`):

```json
{
  "summary": "Resumo executivo do contrato/tarefa analisada",
  "key_findings": [
    "Achado 1 identificado pela análise de IA",
    "Achado 2 identificado pela análise de IA"
  ],
  "metrics": {
    "total_score": 85.5,
    "risk_level": "LOW",
    "calculated_items": 12
  },
  "metadata": {
    "repair_attempts": 1,
    "execution_time_seconds": 3.42,
    "model_used": "gpt-4o-mini"
  }
}
```

---

## 3. Registro de Falha (Coluna `error` na Tabela `tasks`)

Se o Repair Loop esgotar as 3 tentativas ou ocorrer uma falha não recuperável:

- `status`: `"failed"`
- `result`: `null`
- `error`: `"SchemaValidationError: Falha na validação do resultado após 3 tentativas. Erros acumulados: [field 'metrics.total_score': Input should be a valid number]"`
