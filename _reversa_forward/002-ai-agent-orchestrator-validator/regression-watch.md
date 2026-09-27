# Observatório de Regressão: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  

---

## 1. Tabela de Verificação Principal

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|

---

## 2. Histórico de re-extrações

> Nenhuma re-extração executada até o momento.

---

## 3. Arquivadas

> Nenhuma regra arquivada.

---

## 4. Observações (Requisitos Greenfield Implementados)

| ID | Spec de origem | Requisito implementado | Descrição da verificação |
|----|----------------|------------------------|--------------------------|
| W001 | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md#RF-01` | RF-01 | Orquestração da cadeia de agentes executada via `AgentOrchestrator.run_task` |
| W002 | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md#RF-02` | RF-02 | Saída validada obrigatoriamente por Pydantic `AnalysisOutputSchema` |
| W003 | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md#RF-03` | RF-03 | Repair Loop intercepta `ValidationError` e re-prompta até 3 vezes |
| W004 | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md#RF-04` | RF-04 | Cálculos numéricos delegados a `DeterministicTools.calculate_risk_score` |
| W005 | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md#RF-05` | RF-05 | Worker Celery atualiza status no PostgreSQL com o JSON validado |
