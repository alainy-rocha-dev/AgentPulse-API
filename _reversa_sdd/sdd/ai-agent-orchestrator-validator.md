# Spec SDD: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Selo 🟡 PLANEJADO. Especificação técnica de componente gerada por reversa-spec-sdd.

**Versão:** 1.0  
**Data:** 2026-09-27T11:38:37-03:00  
**Componente:** `ai-agent-orchestrator-validator`  
**Status:** Aprovado  

---

## 1. Visão Geral e Problema

🟡 O componente `ai-agent-orchestrator-validator` é o núcleo de inteligência executado pelos Workers Celery. Ele orquestra uma cadeia de agentes de IA (ex: Coletor/Analisador/Redator ou Analista de Contratos) e impõe a técnica de **Anti-Alucinação via Validação Estruturada (Pydantic / Structured Outputs)**, garantindo 0 quebras de schema na gravação de dados no banco.

---

## 2. Requisitos Funcionais (RF)

| ID | Descrição do Requisito | Selo |
|---|---|---|
| **RF-01** | O componente deve executar a cadeia de agentes multiagentes configurada recebendo o contrato/tarefa como entrada. | 🟡 |
| **RF-02** | Toda saída de LLM que será persistida deve passar por validação de schema estrito utilizando Pydantic ou Structured Outputs nativos do provedor (OpenAI / Anthropic / Gemini). | 🟡 |
| **RF-03** | Se o LLM gerar uma resposta fora do formato JSON esperado, o sistema deve acionar automaticamente um "Repair Loop" (re-prompting com erro do Pydantic) de até 3 tentativas. | 🟡 |
| **RF-04** | Cálculos numéricos e estatísticos da cadeia de agentes DEVEM vir de tools Python determinísticas, proibindo a geração livre de números via prompt de texto do LLM. | 🟡 |
| **RF-05** | Após validação bem-sucedida, o resultado estruturado deve ser retornado para gravação imediata no PostgreSQL. | 🟡 |

---

## 3. Escopo e Limites do Componente

### O que está DENTRO (In)
- 🟡 Orquestração da cadeia de agentes (CrewAI / LangGraph)
- 🟡 Definição de ferramentas Python determinísticas (tools)
- 🟡 Mecanismo de Repair Loop anti-alucinação com Pydantic
- 🟡 Formatação estrita do relatório final em JSON + Markdown

### O que está FORA (Out)
- 🟡 Servir requisições HTTP REST
- 🟡 Armazenamento persistente de baixo nível (delegado à camada do PostgreSQL)

---

## 4. Edge Cases e Tratamento de Erros

- 🟡 **Edge Case 1 (Esgotamento das 3 tentativas do Repair Loop):** Se após 3 tentativas a LLM persistir devolvendo JSON inválido, a tarefa falha graciosamente salvando o erro `"SchemaValidationError: Falha na validação do resultado após 3 tentativas"`.
- 🟡 **Edge Case 2 (Erro na API do provedor LLM - Rate Limit/500):** O validador implementa retries com Backoff Exponencial (ex: biblioteca `tenacity`).
- 🟡 **Edge Case 3 (Tentativa do LLM de 'inventar' valores numéricos):** As ferramentas determinísticas validam as entradas e barram a saída se a ferramenta não tiver sido executada.

---

## 5. Critérios de Aceite (Dado / Quando / Então)

- 🟡 **Dado** que uma cadeia de agentes finaliza sua análise, **Quando** o JSON de saída é enviado ao Pydantic, **Então** ele é validado contra o esquema sem levantar exceções.
- 🟡 **Dado** que a LLM retorna um JSON malformado na 1ª tentativa, **Quando** o Repair Loop é acionado com a mensagem de erro da Pydantic, **Then** o LLM corrige o JSON na 2ª tentativa e valida com sucesso.

---

## 6. Avaliação de Qualidade (Score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
SCORE TOTAL: 92/100  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

Breakdown:  
  Completude:    95/100 (peso 30%)  
  Testabilidade: 95/100 (peso 25%)  
  Clareza:       90/100 (peso 20%)  
  Escopo:        90/100 (peso 15%)  
  Edge Cases:    88/100 (peso 10%)  

Gaps críticos: Nenhum. Spec altamente robusta para anti-alucinação.  
Sugestões: Adicionar testes unitários simulando respostas malformadas (mock de LLM).

---
Gerado por reversa-spec-sdd em 2026-09-27T11:38:37-03:00
