# Delta no Modelo de Dados: API Gateway & Gerenciamento de Tarefas Assíncronas

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  

---

## 1. Novas Tabelas

### Tabela `tasks`

Armazena as requisições de tarefas de IA recebidas pela API, seu estado de processamento no worker Celery e o resultado estruturado final.

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    payload JSONB NOT NULL,
    result JSONB NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

---

## 2. Dicionário de Dados

| Campo | Tipo | Nulo? | Descrição |
|-------|------|-------|-----------|
| `id` | UUID | Não | Chave primária única da tarefa (`task_id`) |
| `task_type` | VARCHAR(50) | Não | Tipo da tarefa de IA (ex: `contract_analysis`, `marketing_campaign`) |
| `status` | VARCHAR(20) | Não | Estado atual: `queued`, `processing`, `completed`, `failed` |
| `payload` | JSONB | Não | Parâmetros de entrada da requisição |
| `result` | JSONB | Sim | Resposta estruturada retornada pela cadeia de IA |
| `error_message` | TEXT | Sim | Descrição do erro caso `status = 'failed'` |
| `created_at` | TIMESTAMPTZ | Não | Timestamp ISO da criação da tarefa |
| `updated_at` | TIMESTAMPTZ | Não | Timestamp ISO da última atualização de estado |

---

## 3. Scripts de Migração (Alembic)

O arquivo de migration `versions/001_create_tasks_table.py` será responsável pela criação atômica desta tabela e seus respectivos índices.
