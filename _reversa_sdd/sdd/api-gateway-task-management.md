# Spec SDD: API Gateway e Gerenciamento de Tarefas (`api-gateway-task-management`)

> Selo 🟡 PLANEJADO. Especificação técnica de componente gerada por reversa-spec-sdd.

**Versão:** 1.0  
**Data:** 2026-09-27T11:38:20-03:00  
**Componente:** `api-gateway-task-management`  
**Status:** Aprovado  

---

## 1. Visão Geral e Problema

🟡 O componente `api-gateway-task-management` é o ponto de entrada da aplicação FastAPI. Ele recebe requisições HTTP para criação e consulta de tarefas de agentes de IA, realizando validação rigorosa de entrada via Pydantic e enfileirando o trabalho de forma assíncrona para liberar o cliente em < 500ms com HTTP status 202 Accepted.

---

## 2. Requisitos Funcionais (RF)

| ID | Descrição do Requisito | Selo |
|---|---|---|
| **RF-01** | O sistema deve expor um endpoint `POST /tasks` para recepção do payload da tarefa de IA. | 🟡 |
| **RF-02** | O payload recebido em `POST /tasks` deve ser validado estritamente via modelo Pydantic (`TaskCreateSchema`). | 🟡 |
| **RF-03** | Em caso de sucesso na validação e enfileiramento, a API deve retornar HTTP 202 Accepted com `task_id` (UUIDv4) e status `"queued"`. | 🟡 |
| **RF-04** | O sistema deve expor um endpoint `GET /tasks/{task_id}` para consulta do status (`queued`, `running`, `completed`, `failed`) e resultado da tarefa. | 🟡 |
| **RF-05** | Em caso de payload inválido no `POST /tasks`, a API deve retornar HTTP 422 Unprocessable Entity detalhando os campos incorretos. | 🟡 |

---

## 3. Escopo e Limites do Componente

### O que está DENTRO (In)
- 🟡 Validação de esquema JSON de entrada usando Pydantic
- 🟡 Geração de UUIDv4 único para identificação da tarefa
- 🟡 Disparo do job assíncrono para a fila Celery
- 🟡 Resposta HTTP 202 com contrato padronizado
- 🟡 Consulta síncrona do estado da tarefa no PostgreSQL

### O que está FORA (Out)
- 🟡 Execução da cadeia de agentes de IA (responsabilidade do `ai-agent-orchestrator-validator`)
- 🟡 Gerenciamento interno de workers do Celery (responsabilidade do `task-queue-broker`)

---

## 4. Edge Cases e Tratamento de Erros

- 🟡 **Edge Case 1 (Task ID inexistente):** `GET /tasks/{uuid_invalido}` deve retornar HTTP 404 Not Found com mensagem `"Tarefa não encontrada"`.
- 🟡 **Edge Case 2 (Falha de comunicação com Redis/Broker):** Se o broker estiver inacessível durante o `POST /tasks`, a API deve capturar a exceção e responder HTTP 503 Service Unavailable sem deixar conexões pendentes.
- 🟡 **Edge Case 3 (Payload gigante/incompatível):** Bloqueio no Pydantic antes de alocar recursos no Redis.

---

## 5. Critérios de Aceite (Dado / Quando / Então)

- 🟡 **Dado** que um cliente envia um JSON válido para `POST /tasks`, **Quando** a API recebe a requisição, **Então** retorna HTTP 202 com `{"task_id": "<UUID>", "status": "queued"}` em menos de 500ms.
- 🟡 **Dado** uma tarefa salva no banco com status "completed", **Quando** o cliente consulta `GET /tasks/{task_id}`, **Então** a API retorna status 200 OK com o JSON contendo o resultado da análise de IA.

---

## 6. Avaliação de Qualidade (Score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
SCORE TOTAL: 88/100  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

Breakdown:  
  Completude:    90/100 (peso 30%)  
  Testabilidade: 90/100 (peso 25%)  
  Clareza:       85/100 (peso 20%)  
  Escopo:        85/100 (peso 15%)  
  Edge Cases:    85/100 (peso 10%)  

Gaps críticos: Nenhum identificado. Spec testável e completa.  
Sugestões: Incluir testes de carga unitários com pytest-asyncio.

---
Gerado por reversa-spec-sdd em 2026-09-27T11:38:20-03:00
