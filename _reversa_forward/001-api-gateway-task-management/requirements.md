# Requirements: API Gateway & Gerenciamento de Tarefas Assíncronas

> Identificador: `001-api-gateway-task-management`  
> Data: `2026-09-27`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

O componente API Gateway expõe os endpoints HTTP principais do sistema FastAPI. Ele recebe requisições de submissão de tarefas de IA de longa duração, valida a estrutura dos dados de entrada via Pydantic, publica o job na fila Redis (Celery) e retorna imediatamente HTTP 202 Accepted com um `task_id`. Também permite a consulta assíncrona do status e do resultado da execução através do endpoint GET `/tasks/{task_id}`.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4-escopo-in` | Submissão de tarefas assíncronas POST /tasks e consulta GET /tasks/{task_id} | 🟡 |
| `_reversa_sdd/sdd/api-gateway-task-management.md` | Especificação técnica dos schemas Pydantic e controladores FastAPI | 🟡 |
| `_reversa_sdd/sdd/task-queue-broker.md` | Despacho de mensagens para o Redis/Celery Broker | 🟡 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Engenheiro Backend / Dev IA | Submeter tarefas de IA sem sofrer timeouts HTTP | Cliente envia um payload de solicitação para POST `/tasks` e recebe resposta imediata para polling posterior |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Ao receber uma requisição válida em `POST /tasks`, a API deve gerar um identificador único `task_id` (UUIDv4), persistir o estado inicial como `queued` e retornar resposta HTTP 202 Accepted em menos de 500ms. 🟡
2. **RN-02:** Payloads inválidos na requisição `POST /tasks` devem ser rejeitados imediatamente pela camada Pydantic com código HTTP 422 Unprocessable Entity contendo os detalhes das falhas de validação. 🟡
3. **RN-03:** A requisição `GET /tasks/{task_id}` deve consultar o banco de dados PostgreSQL/Redis e retornar o estado atual da tarefa (`queued`, `processing`, `completed`, `failed`). Quando o estado for `completed`, deve retornar o resultado estruturado da execução. 🟡
4. **RN-04:** Caso o `task_id` informado em `GET /tasks/{task_id}` não seja encontrado na base, a API deve retornar HTTP 404 Not Found. 🟡
5. **RN-05:** O tamanho máximo de payload (texto/JSON de entrada) aceito no endpoint `POST /tasks` é de 10 MB. Requisições que excederem este limite devem ser rejeitadas com HTTP 413 Payload Too Large. 🟢

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar endpoint `POST /tasks` para recepção de requisições de IA | Must | Aceitar payload JSON e validar via Pydantic | 🟡 |
| RF-02 | Publicar tarefa na fila Celery/Redis após validação do payload | Must | Job publicado no Redis com `task_id` correspondente | 🟡 |
| RF-03 | Retornar HTTP 202 Accepted com `task_id` e status `queued` | Must | Tempo de resposta < 500ms com schema de resposta correto | 🟡 |
| RF-04 | Criar endpoint `GET /tasks/{task_id}` para consulta de status e resultado | Must | Retornar status atualizado e payload de resultado se finalizado | 🟡 |
| RF-05 | Lidar com falhas de validação e registros inexistentes | Must | Retornar HTTP 422 para payload inválido e HTTP 404 para `task_id` inexistente | 🟡 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Latência do endpoint POST `/tasks` < 500ms | Resposta assíncrona evita travamento da conexão do cliente | 🟡 |
| Confiabilidade | Garantir enfileiramento sem perda de requisições | Tarefas publicadas no Redis de forma síncrona antes da resposta HTTP 202 | 🟡 |
| Validação | Validação estrita via Pydantic v2 | Prevenção de alucinação ou injeção de dados malformatados no worker | 🟡 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Submissão bem-sucedida de tarefa de IA
  Dado que um cliente envia um payload JSON válido para POST /tasks
  Quando o API Gateway valida a requisição
  Então o job é publicado na fila Celery/Redis
  E a API responde com HTTP 202 Accepted contendo task_id e status "queued" em menos de 500ms

Cenário: Tentativa de submissão com payload inválido
  Dado que um cliente envia um JSON malformatado ou sem campos obrigatórios para POST /tasks
  Quando o API Gateway processa a requisição
  Então a camada Pydantic rejeita a requisição
  E a API retorna HTTP 422 Unprocessable Entity com a descrição dos erros

Cenário: Polling de tarefa concluída
  Dado que uma tarefa com task_id "123e4567-e89b-12d3-a456-426614174000" foi finalizada pelo worker
  Quando o cliente faz requisição GET /tasks/123e4567-e89b-12d3-a456-426614174000
  Então a API retorna HTTP 200 OK com status "completed" e o resultado em formato JSON
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (POST /tasks) | Must | Funcionalidade core de entrada do sistema |
| RF-02 (Enfileiramento Redis) | Must | Essencial para o processamento assíncrono |
| RF-03 (HTTP 202 Accepted) | Must | Contrato da API para comunicação assíncrona |
| RF-04 (GET /tasks/{task_id}) | Must | Permite ao cliente acompanhar e obter os resultados |
| RF-05 (Tratamento de erros 422/404) | Must | Garante estabilidade e contrato limpo de erros |

---

## 9. Esclarecimentos

### Sessão 2026-09-27
- **Q:** Qual o limite máximo de tamanho de payload (bytes/tokens) aceito no endpoint `POST /tasks` para evitar abuso de memória?
- **R:** 10 MB (suficiente para contratos longos e briefings extensos).

---

## 10. Lacunas

> Nenhuma lacuna pendente. Todas as dúvidas foram esclarecidas.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-09-27 | Esclarecimento sobre limite de payload de 10 MB via `/reversa-clarify` | reversa-clarify |
