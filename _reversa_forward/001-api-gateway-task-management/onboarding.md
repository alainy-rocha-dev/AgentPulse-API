# Guia de Onboarding e Validação: API Gateway

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  

---

## 1. Pré-requisitos

- Docker & Docker Compose instalados.
- Python 3.11+ (para execução local fora do container, se desejado).
- Cliente HTTP (`curl`, Postman, ou interface Swagger).

---

## 2. Passo a Passo de Teste Executável

### Passo 1: Subir os serviços via Docker Compose
```bash
docker-compose up -d --build
```
Verifique se a API (porta 8000), Redis (porta 6379) e PostgreSQL (porta 5432) estão rodando com status healthy.

### Passo 2: Submeter uma Tarefa de IA
Execute o comando cURL abaixo para submeter uma tarefa:

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "contract_analysis",
    "payload": {
      "contract_text": "Este é um contrato de teste para validação da API assíncrona."
    }
  }'
```

**Resposta Esperada (HTTP 202 Accepted):**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "queued",
  "message": "Tarefa recebida e enfileirada com sucesso."
}
```

### Passo 3: Consultar o Status da Tarefa
Utilize o `task_id` retornado no passo anterior para consultar o endpoint GET:

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000"
```

**Resposta Esperada (HTTP 200 OK):**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "queued",
  "result": null,
  "created_at": "2026-09-27T11:42:00Z"
}
```

---

## 3. Testes de Casos Negativos

### Teste A: Payload malformatado (HTTP 422)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{}'
```
*Deve retornar HTTP 422 Unprocessable Entity.*

### Teste B: Payload excedendo 10 MB (HTTP 413)
*Tentar enviar um payload com tamanho superior a 10 MB. Deve retornar HTTP 413 Payload Too Large.*

### Teste C: Task ID Inexistente (HTTP 404)
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/00000000-0000-0000-0000-000000000000"
```
*Deve retornar HTTP 404 Not Found.*
