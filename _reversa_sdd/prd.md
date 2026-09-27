# PRD: AgentPulse API (`agent-pulse-api`) - API de Automação de Agentes com Validação (Back-end)

> Selo 🟡 PLANEJADO. Documento gerado a partir de ideation + personas.

**Versão:** 1.0
**Data:** 2026-09-27T11:37:40-03:00
**Autor:** reversa-drafter
**Status:** rascunho

---

## 1. Problema

🟡 A API resolve a necessidade de executar tarefas de IA de longa duração (ex: análise de contratos ou criação de campanhas de marketing) de forma assíncrona, devolvendo uma resposta imediata (202 Accepted + ID de tarefa) para evitar timeouts HTTP.

### Quem sente
🟡 Engenheiros Backend e Desenvolvedores de IA ao tentarem integrar agentes de IA em ambientes de produção sem travar conexões HTTP nem sofrer com erros de persistência causados por respostas não-determinísticas.

---

## 2. Personas-alvo

🟡 Referência completa em [`personas.md`](./personas.md). Resumo:

- **Engenheiro Backend / Desenvolvedor de IA**: 🟡 Precisa expor tarefas assíncronas de longa duração de agentes de IA via API HTTP robusta com validação Pydantic e persistência em PostgreSQL.

---

## 3. Métricas de sucesso

🟡 Medição de estabilidade e resiliência no processamento de requisições de agentes de IA.

| Métrica | Unidade | Alvo | Prazo |
|---|---|---|---|
| 🟡 Processamento Assíncrono | % de requisições sem timeout HTTP | 100% | 3 meses |
| 🟡 Validação de Schema | Erros de validação/quebra no PostgreSQL | 0 falhas | 3 meses |
| 🟡 Reprodutibilidade de Infra | Tempo para subir a stack via Docker | < 2 min | 3 meses |

---

## 4. Escopo (in)

🟡 Funcionalidades e componentes que fazem parte do MVP do Projeto 3:

- 🟡 Endpoint POST /tasks para submissão de tarefas de IA com validação de payload via Pydantic
- 🟡 Retorno imediato HTTP 202 Accepted contendo `task_id` e status "queued"
- 🟡 Fila de mensageria com Redis e Workers Celery para processamento assíncrono em segundo plano
- 🟡 Execução de fluxo multiagentes de IA no worker (análise de contratos ou campanha de marketing)
- 🟡 Validação anti-alucinação de saída estruturada via Pydantic / Structured Outputs (OpenAI/Gemini/Anthropic)
- 🟡 Persistência do histórico e resultado final no PostgreSQL
- 🟡 Endpoint GET /tasks/{task_id} para consulta de status e resultado
- 🟡 Containerização com Docker Compose (API, Redis, Worker Celery, PostgreSQL)
- 🟡 Documentação técnica no README com Diagrama de Arquitetura Mermaid e explicação sobre saídas não-determinísticas

---

## 5. Não-objetivos (out)

🟡 O que está explicitamente fora do escopo deste projeto:

- 🟡 Construção de interface frontend dedicada em React/Vue (utilizar a UI automática Swagger/OpenAPI do FastAPI)
- 🟡 Deploy automatizado em provedores de nuvem gerenciados (o foco é a infraestrutura reproduzível local via Docker Compose)
- 🟡 Sistema completo de autenticação OAuth2/JWT multi-tenant (foco em arquitetura de tarefas e validação)

---

## 6. Restrições

🟡 Especificações obrigatórias de tecnologia e ambiente:

| Tipo | Descrição |
|---|---|
| 🟡 Técnica | Python 3.11+, FastAPI, Celery, Redis, PostgreSQL, Pydantic, Docker Compose |
| 🟡 Prazo | [INDEFINIDO, validar com usuário] |
| 🟡 Compliance | Garantir sanitização de saídas para prevenir SQL Injection ou gravação de dados corrompidos |
| 🟡 Orçamento | Utilizar modelos LLM compactos/econômicos para testes em desenvolvimento |

---

## 7. Dependências externas

🟡 Serviços e APIs necessárias:

- 🟡 API de Provedor de LLM (OpenAI / Anthropic / Google Gemini) para execução da cadeia de agentes
- 🟡 Imagens oficiais Docker (Python, Redis, PostgreSQL)

---

## 8. Riscos

🟡 Riscos identificados e planos de mitigação:

| Risco | Impacto | Probabilidade | Mitigação proposta |
|---|---|---|---|
| 🟡 Perda de tarefas no broker Redis | Alto | Baixa | Configurar persistência AOF/RDB no Redis ou usar retries no Celery |
| 🟡 Resposta LLM fora do formato JSON exigido | Alto | Média | Utilizar Structured Outputs nativo / Pydantic com loop de reparo de 2-3 tentativas |
| 🟡 Incompatibilidade de ambiente de execução | Médio | Baixa | Orquestração centralizada via Docker Compose com healthchecks |

---

## 9. Critérios de aceite (alto nível)

🟡 Validação dos fluxos principais da API:

- 🟡 **Dado** que um cliente envia POST /tasks com um contrato para análise, **Quando** a requisição for processada, **Então** o sistema responde em < 500ms com HTTP 202 contendo um `task_id`.
- 🟡 **Dado** que um Worker Celery finaliza a cadeia de agentes, **Quando** a saída for validada pelo Pydantic, **Então** o resultado final é salvo no PostgreSQL com status "completed".
- 🟡 **Dado** que o cliente faz GET /tasks/{task_id}, **Quando** a tarefa estiver concluída, **Então** a API retorna o resultado estruturado em JSON conforme a especificação.

---

## Pendências de cobertura

🟡 Nenhuma pendência crítica. Seção de prazo mantida como `[INDEFINIDO]` para acompanhamento contínuo.

---

Gerado por reversa-drafter em 2026-09-27T11:37:40-03:00
Fontes: ideation.md, personas.md
