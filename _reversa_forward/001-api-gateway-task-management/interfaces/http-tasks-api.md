# Contrato de Interface: HTTP Tasks API

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  
> Tipo: `HTTP / REST`  

---

## 1. Endpoint: Submissão de Tarefa (`POST /api/v1/tasks`)

Recepção e validação de solicitação de execução assíncrona de agente de IA.

### Request
- **Método:** `POST`
- **Path:** `/api/v1/tasks`
- **Headers:** `Content-Type: application/json`
- **Tamanho Máximo de Body:** 10 MB

#### Body Schema (`TaskCreate`)
```json
{
  "task_type": "contract_analysis",
  "payload": {
    "contract_text": "string (obrigatório)"
  }
}
```

### Responses

#### 202 Accepted
```json
{
  "task_id": "UUID (ex: 123e4567-e89b-12d3-a456-426614174000)",
  "status": "queued",
  "message": "Tarefa recebida e enfileirada com sucesso."
}
```

#### 413 Payload Too Large
```json
{
  "detail": "O tamanho do payload excede o limite máximo permitido de 10 MB."
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "task_type"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 2. Endpoint: Consulta de Status (`GET /api/v1/tasks/{task_id}`)

Consulta o estado atual e o resultado da tarefa.

### Request
- **Método:** `GET`
- **Path:** `/api/v1/tasks/{task_id}`
- **Path Params:** `task_id` (UUID format)

### Responses

#### 200 OK
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_type": "contract_analysis",
  "status": "completed",
  "result": {
    "summary": "Análise concluída",
    "risk_score": "low",
    "key_clauses": []
  },
  "error_message": null,
  "created_at": "2026-09-27T11:40:00Z",
  "updated_at": "2026-09-27T11:40:15Z"
}
```

#### 404 Not Found
```json
{
  "detail": "Tarefa com o ID informado não foi encontrada."
}
```
