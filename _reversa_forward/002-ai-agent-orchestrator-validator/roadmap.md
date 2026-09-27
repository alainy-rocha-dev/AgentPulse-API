# Roadmap: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Identificador: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  
> Requirements: `_reversa_forward/002-ai-agent-orchestrator-validator/requirements.md`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA  

---

## 1. Resumo da abordagem

Implementação da camada de execução e orquestração de agentes de IA consumidos pelo Celery Worker (`app/worker.py`). A arquitetura baseia-se em um orquestrador modular (`app/services/agent_orchestrator.py`), schemas Pydantic v2 estritos de entrada/saída (`app/schemas/agent_output.py`), ferramentas Python determinísticas (`app/services/tools.py`), e um Repair Loop resiliente (`app/services/repair_loop.py`) com retries via `tenacity` e re-prompting estruturado em até 3 tentativas. O resultado final validado ou o traceback de erro é persistido no PostgreSQL atualizando a tabela `tasks`.

---

## 2. Princípios aplicados

| Princípio | Como a feature se relaciona | Status |
|-----------|------------------------------|--------|
| Anti-Alucinação via Schema Estrito | Garante 0 gravação de JSON malformado através do Pydantic v2 | respeita |
| Determinismo Numérico | Cálculos matemáticos/estatísticos delegados estritamente a ferramentas Python | respeita |
| Resiliência e Graceful Failure | Repair Loop de 3 tentativas + retry com backoff exponencial (`tenacity`) | respeita |

---

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Validação Pydantic v2 no Repair Loop | Feedback direto do schema `ValidationError` em formato legível ao LLM | Regex parsing, validação via JSON Schema genérico | 🟢 |
| D-02 | Execução de Tools Python via wrappers determinísticos | Impede que a LLM compute operações numéricas internamente no prompt | Prompt engineering simples sem call-out | 🟢 |
| D-03 | Tenacity para Backoff Exponencial em chamadas de LLM | Tratamento de rate limits (HTTP 429) e erros 5xx de forma limpa e configurável | `time.sleep` manual, retry do Celery no job inteiro | 🟢 |
| D-04 | Atualização síncrona/assíncrona do status no PostgreSQL ao fim da cadeia | Celery worker executa tarefa isolada, garantindo idempotência e transação limpa | Long polling HTTP no worker | 🟢 |

---

## 4. Premissas

| Premissa | Origem (`requirements.md` seção) | Risco se errada |
|----------|----------------------------------|-----------------|
| O Celery Worker consome o payload do job contendo `task_id` e `input_data` | `requirements.md` Seção 2 | Falha na captura do parâmetro de entrada da tarefa |
| Chaves de API de LLM serão lidas de variáveis de ambiente (`OPENAI_API_KEY`, etc.) | `requirements.md` Seção 6 | Exceção de autenticação ao conectar com o provedor de LLM |

---

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| `ai-agent-orchestrator-validator` | `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | componente-novo | Criar `app/services/agent_orchestrator.py`, `app/schemas/agent_output.py`, `app/services/repair_loop.py` e `app/services/tools.py`. |
| `task-queue-broker` | `_reversa_sdd/sdd/task-queue-broker.md` | regra-alterada | Atualizar `app/worker.py` para invocar o `agent_orchestrator.run_task` no Celery job. |
| `postgres-persistence-container` | `_reversa_sdd/sdd/postgres-persistence-container.md` | regra-alterada | Atualizar registro da tarefa no PostgreSQL com o payload validado ou mensagem de erro. |

---

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma migração de banco de dados necessária (schema da tabela `tasks` criado na Feature 001 suporta `result` em JSONB e `error` em String).
- Detalhe completo em: `_reversa_forward/002-ai-agent-orchestrator-validator/data-delta.md`

---

## 7. Delta de contratos externos

| Contrato | Tipo | Arquivo de detalhe |
|----------|------|--------------------|
| Celery Task Payload / Result | Fila (Celery Redis) | `_reversa_forward/002-ai-agent-orchestrator-validator/interfaces/agent-worker-interface.md` |

---

## 8. Plano de migração

n/a (sem quebra de compatibilidade ou migração de dados existente).

---

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| LLM persistir em JSON malformado | alto | baixo | Repair Loop com até 3 tentativas injetando o traceback exato do Pydantic + fallback para status `failed` |
| Latência ou Rate Limit na API de LLM | médio | médio | Backoff exponencial via `tenacity` e timeout limite por requisição |

---

## 10. Critério de pronto

- [ ] Todas as ações do `actions.md` marcadas `[X]`
- [ ] Módulos `app/schemas/agent_output.py`, `app/services/repair_loop.py`, `app/services/tools.py`, `app/services/agent_orchestrator.py` criados com testes unitários
- [ ] Worker Celery (`app/worker.py`) integrado e testado fim a fim
- [ ] Testes automatizados cobrindo sucesso na 1ª tentativa, sucesso no Repair Loop (2ª tentativa) e falha graciosa na 3ª tentativa

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-plan` | reversa-plan |
