# Regression Watch: API Gateway & Gerenciamento de Tarefas Assíncronas

> Feature: `001-api-gateway-task-management`  
> Data: `2026-09-27`  
> Nota de Âncora: Greenfield (specs SDD).  

---

## 1. Watch List Principal (Regras de Negócio Legado)

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|
| - | n/a (greenfield) | n/a | n/a | n/a |

---

## 2. Observações (Requisitos da Feature Greenfield)

- **RF-01 / RF-02 / RF-03:** Endpoint `POST /tasks` deve aceitar JSON válido, limitar payload a 10 MB, enfileirar job no Celery e retornar HTTP 202 com `task_id`.
- **RF-04:** Endpoint `GET /tasks/{task_id}` deve retornar o status (`queued`, `processing`, `completed`, `failed`) e o resultado estruturado em JSON.
- **RF-05:** Erros de validação devem retornar HTTP 422, limite > 10MB deve retornar HTTP 413, e ID inexistente HTTP 404.

---

## 3. Histórico de Re-extrações

> Nenhuma re-extração executada ainda.

---

## 4. Arquivadas

> Nenhuma regra arquivada.
