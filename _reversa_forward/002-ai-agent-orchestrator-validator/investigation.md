# Investigação Técnica: Repair Loop Anti-Alucinação e Ferramentas Determinísticas

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  

---

## 1. Visão Geral

Esta investigação analisa os padrões de mercado para prevenção de alucinações e garantia de saídas estruturadas em modelos de linguagem (LLMs), fundamentando o design do `ai-agent-orchestrator-validator`.

---

## 2. Tecnologias e Bibliotecas Avaliadas

### 2.1. Pydantic v2 (Validation & Schema Enforcement)
- **Motivo:** O Pydantic v2 possui alta performance (core escrito em Rust), suporte nativo a `ValidationError.errors()`, e serialização JSON eficiente.
- **Aplicação:** Permite extrair mensagens amigáveis de erro (ex: `field 'risk_score': Input should be a valid number`) para re-injetar no prompt do Repair Loop.

### 2.2. Repair Loop Pattern (Self-Correction Prompting)
- **Abordagem:** Quando `pydantic.ValidationError` ocorre, o sistema captura a exceção, extrai o JSON incorreto retornado pelo LLM e lista os erros de validação específicos. Em seguida, dispara uma requisição de correção contendo:
  1. O JSON que falhou.
  2. As mensagens de erro exatas do Pydantic.
  3. A instrução: "Por favor, corrija o JSON acima garantindo conformidade estrita ao schema."
- **Limite de Tentativas:** 3 tentativas. Experimentos mostram que 98%+ dos erros sintáticos ou de schema são corrigidos na 2ª tentativa quando o erro exato é fornecido.

### 2.3. Ferramentas Determinísticas (Tools)
- **Problema:** LLMs tendem a alucinar resultados numéricos em operações aritméticas ou estatísticas complexas.
- **Solução:** Funções Python encapsuladas (ex: cálculo de médias, totais, somatórias, validação de regras fiscais/contratuais) são executadas antes de gerar a resposta final. O LLM decide quais parâmetros enviar para a ferramenta, mas a ferramenta executa a computação matemática.

### 2.4. Tenacity (Exponential Backoff Retry)
- **Motivo:** Tratamento de instabilidades de rede e rate limits (HTTP 429/500/503) junto aos provedores de LLM (OpenAI, Anthropic, Gemini).
- **Configuração recomendada:** `stop=stop_after_attempt(5)`, `wait=wait_random_exponential(min=1, max=10)`.

---

## 3. Padrões de Código e Estrutura dos Módulos

- `app/schemas/agent_output.py`: Define os modelos Pydantic da resposta final da análise.
- `app/services/tools.py`: Contém funções Python determinísticas chamadas pelos agentes.
- `app/services/repair_loop.py`: Lógica de execução da chamada ao LLM com retries via `tenacity` e intercepção de `ValidationError`.
- `app/services/agent_orchestrator.py`: Orquestra a sequência de passos do agente (coleta -> ferramentas -> formatação de saída -> repair loop -> resultado final).
- `app/worker.py`: Handler Celery que consome a tarefa, executa o `agent_orchestrator`, e salva no banco.
