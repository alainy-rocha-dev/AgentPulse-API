# Impacto no Legado: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  
> Âncora de contexto: Feature greenfield, sem legado pré-existente. Âncora: `prd.md` + specs em `_reversa_sdd/sdd/`.  
> Política de edição: `allowLegacyEdits: true`, `allowedPaths: []` (Liberação irrestrita).  

---

## 1. Tabela de Arquivos Afetados

| Arquivo afetado | Componente | Tipo de impacto | Severidade | Justificativa |
|-----------------|------------|-----------------|------------|---------------|
| `app/schemas/agent_output.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Modelos Pydantic v2 para validação estruturada do resultado da análise |
| `app/services/tools.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Funções determinísticas em Python para cálculo estatístico e numérico |
| `app/services/repair_loop.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Loop anti-alucinação de até 3 tentativas com traceback Pydantic |
| `app/services/agent_orchestrator.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Orquestrador principal da cadeia multiagentes |
| `app/worker.py` | `_reversa_sdd/sdd/task-queue-broker.md` | `regra-alterada` | LOW | Integração do worker Celery com o `AgentOrchestrator` e atualização de status/resultado |
| `tests/test_schemas_and_tools.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Cobertura de testes dos schemas e ferramentas |
| `tests/test_repair_loop.py` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | `componente-novo` | LOW | Testes unitários do Repair Loop e tratamento de exaustão |
| `tests/test_worker_orchestrator_integration.py` | `_reversa_sdd/sdd/task-queue-broker.md` | `componente-novo` | LOW | Testes de integração do worker Celery com orquestração |

---

## 2. Diff Conceitual por Componente

- **`ai-agent-orchestrator-validator`**: Implementada a camada completa de inteligência com schema Pydantic, Repair Loop com re-prompting e ferramentas Python para 0 alucinações numéricas.
- **`task-queue-broker`**: O worker Celery em `app/worker.py` foi estendido para invocar o orquestrador e gravar o resultado estruturado ou mensagem de exceção `SchemaValidationError` no PostgreSQL.

---

## 3. Regras Preservadas

> Feature greenfield: sem regras extraídas de código legado pré-existente.

---

## 4. Regras Modificadas

> Feature greenfield: sem regras de legado modificadas.
