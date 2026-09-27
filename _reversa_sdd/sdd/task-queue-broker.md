# Spec SDD: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Selo 🟡 PLANEJADO. Especificação técnica de componente gerada por reversa-spec-sdd.

**Versão:** 1.0  
**Data:** 2026-09-27T11:38:25-03:00  
**Componente:** `task-queue-broker`  
**Status:** Aprovado  

---

## 1. Visão Geral e Problema

🟡 O componente `task-queue-broker` gerencia a infraestrutura de mensageria assíncrona baseada em Redis e Celery/ARQ. Ele é responsável por transportar com segurança as mensagens de solicitação da API FastAPI até os Workers, garantindo concorrência, suporte a retentativas em caso de falha transitória e isolamento completo do ciclo de vida da requisição HTTP.

---

## 2. Requisitos Funcionais (RF)

| ID | Descrição do Requisito | Selo |
|---|---|---|
| **RF-01** | O broker Redis deve manter a fila de tarefas (`celery` / `default`) de forma persistente com RDB/AOF para evitar perda de mensagens. | 🟡 |
| **RF-02** | O sistema de mensageria deve transicionar o estado da tarefa para `"running"` no momento exato em que um Worker Celery consome o job. | 🟡 |
| **RF-03** | O worker deve ter tempo máximo de execução por tarefa (`task_time_limit` de 300 segundos) para prevenir bloqueios e loops infinitos. | 🟡 |
| **RF-04** | Caso o Worker Celery caia durante o processamento, o job deve ser automaticamente reenfileirado (mecanismo de ack tardio / `acks_late`). | 🟡 |
| **RF-05** | Em falha de execução não-recuperável, o estado da tarefa no PostgreSQL deve ser atualizado para `"failed"` com o traceback de erro sanitizado. | 🟡 |

---

## 3. Escopo e Limites do Componente

### O que está DENTRO (In)
- 🟡 Configuração e conteinerização do Redis Broker
- 🟡 Configuração das filas, concorrência de workers e retries do Celery
- 🟡 Gerenciamento de timeouts de tarefas longas de IA
- 🟡 Atualizações do estado da tarefa no broker e banco

### O que está FORA (Out)
- 🟡 Validação de regras de negócio das LLMs
- 🟡 Recebimento direto de requisições HTTP públicas

---

## 4. Edge Cases e Tratamento de Erros

- 🟡 **Edge Case 1 (Estouro de memória no Redis):** Política de expiração `volatile-lru` ativada para garantir disponibilidade do broker.
- 🟡 **Edge Case 2 (Crash do Worker por OOM/Timeout):** Captura do sinal `SIGKILL` pelo Celery para transicionar tarefa para `"failed"` em vez de deixá-la travada em `"running"`.
- 🟡 **Edge Case 3 (Desconexão temporária com PostgreSQL):** Retentativa exponencial do worker ao tentar gravar o resultado final.

---

## 5. Critérios de Aceite (Dado / Quando / Então)

- 🟡 **Dado** que uma tarefa é enfileirada via FastAPI, **Quando** o Redis recebe a mensagem, **Então** o Worker Celery consome o job em menos de 100ms em ambiente ocioso.
- 🟡 **Dado** que um agente excede o limite de 300s, **Quando** o `task_time_limit` expira, **Então** o Celery interrompe o processo e registra a tarefa como "failed".

---

## 6. Avaliação de Qualidade (Score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
SCORE TOTAL: 86/100  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

Breakdown:  
  Completude:    88/100 (peso 30%)  
  Testabilidade: 85/100 (peso 25%)  
  Clareza:       85/100 (peso 20%)  
  Escopo:        88/100 (peso 15%)  
  Edge Cases:    85/100 (peso 10%)  

Gaps críticos: Nenhum.  
Sugestões: Configurar monitoramento com Flower (opcional).

---
Gerado por reversa-spec-sdd em 2026-09-27T11:38:25-03:00
