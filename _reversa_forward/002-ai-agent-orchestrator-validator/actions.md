# Actions: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Identificador: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  
> Roadmap: `_reversa_forward/002-ai-agent-orchestrator-validator/roadmap.md`  

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de ações | 9 |
| Paralelizáveis (`[//]`) | 5 |
| Maior cadeia de dependência | 5 |

## Fase 1, Preparação

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T001 | Criar schema Pydantic `AnalysisOutputSchema` para saída estruturada em `app/schemas/agent_output.py` | - | `[//]` | `app/schemas/agent_output.py` | 🟢 | `[X]` |
| T002 | Criar módulo de ferramentas Python determinísticas para cálculos e métricas estatísticas em `app/services/tools.py` | - | `[//]` | `app/services/tools.py` | 🟢 | `[X]` |

## Fase 2, Testes

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T003 | Criar suíte de testes unitários para schemas Pydantic e ferramentas determinísticas em `tests/test_schemas_and_tools.py` | T001, T002 | `[//]` | `tests/test_schemas_and_tools.py` | 🟢 | `[X]` |
| T004 | Criar suíte de testes unitários para o Repair Loop anti-alucinação com mocks de LLM em `tests/test_repair_loop.py` | T001 | `[//]` | `tests/test_repair_loop.py` | 🟢 | `[X]` |

## Fase 3, Núcleo

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T005 | Implementar o serviço de Repair Loop anti-alucinação com Pydantic v2 e retries `tenacity` em `app/services/repair_loop.py` | T001, T002 | - | `app/services/repair_loop.py` | 🟢 | `[X]` |
| T006 | Implementar o Orquestrador de Agentes de IA integrando ferramentas, repair loop e validação em `app/services/agent_orchestrator.py` | T005 | - | `app/services/agent_orchestrator.py` | 🟢 | `[X]` |

## Fase 4, Integração

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T007 | Atualizar o Celery Worker (`app/worker.py`) para invocar o orquestrador e persistir resultados/erros no PostgreSQL | T006 | - | `app/worker.py` | 🟢 | `[X]` |
| T008 | Criar teste de integração E2E do Celery worker com orquestrador e atualização de status em `tests/test_worker_orchestrator_integration.py` | T007 | `[//]` | `tests/test_worker_orchestrator_integration.py` | 🟢 | `[X]` |

## Fase 5, Polimento

| ID | Descrição | Dependências | Paralelismo | Arquivo alvo | Confidência | Status |
|----|-----------|--------------|-------------|--------------|-------------|--------|
| T009 | Adicionar logging detalhado e métricas de tentativas de reparo do Repair Loop em `app/services/agent_orchestrator.py` | T007 | - | `app/services/agent_orchestrator.py` | 🟢 | `[X]` |

## Notas de execução

## Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-to-do` | reversa-to-do |
