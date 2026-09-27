# Requirements: Orquestrador de Agentes de IA e Validador (`ai-agent-orchestrator-validator`)

> Identificador: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA  

---

## 1. Resumo executivo

O componente `ai-agent-orchestrator-validator` é o núcleo de inteligência executado pelos Workers Celery. Ele orquestra a cadeia de agentes de IA para processamento de tarefas assíncronas (como análise de contratos ou criação de campanhas) e impõe a técnica de **Anti-Alucinação via Validação Estruturada (Pydantic / Structured Outputs)**, garantindo 0 quebras de schema na gravação de dados no PostgreSQL e fornecendo um Repair Loop de até 3 tentativas para correção automática de JSONs malformados retornados pelas LLMs.

---

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/prd.md#4-escopo-in` | Execução de fluxo multiagentes de IA no worker e validação anti-alucinação de saída estruturada | 🟡 |
| `_reversa_sdd/sdd/ai-agent-orchestrator-validator.md` | Especificação técnica completa da cadeia de orquestração e Repair Loop | 🟡 |
| `_reversa_sdd/addenda/001-api-gateway-task-management.md` | O Worker Celery (`app/worker.py`) consome os jobs publicados pelo API Gateway | 🟢 |

---

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Engenheiro Backend / Dev IA | Executar tarefas de IA de alta confiabilidade sem dados corrompidos | O worker Celery consome o job, executa a cadeia de agentes, valida o schema JSON de saída e salva o resultado final sanitizado no banco |

---

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Toda execução de cadeia de agentes deve receber o payload da tarefa e produzir um resultado final estruturado em Pydantic. 🟡
2. **RN-02 (Repair Loop):** Se o LLM gerar uma resposta com schema JSON inválido, o sistema deve reinvocar automaticamente a API de LLM enviando a mensagem exata de erro do Pydantic, permitindo até 3 tentativas de correção. 🟡
3. **RN-03 (Edge Case - Falha no Repair Loop):** Se após 3 tentativas o LLM persistir devolvendo JSON inválido, a tarefa deve falhar graciosamente com o erro `"SchemaValidationError: Falha na validação do resultado após 3 tentativas"` e status `failed`. 🟢
4. **RN-04 (Ferramentas Determinísticas):** Cálculos numéricos e estatísticos da cadeia de agentes DEVEM vir de tools Python determinísticas, proibindo a geração livre de números via prompt de texto do LLM. 🟡
5. **RN-05 (Resiliência de Rede):** Chamadas às APIs de LLM devem utilizar retry com backoff exponencial via `tenacity` para lidar com instabilidades temporárias e Rate Limits (HTTP 429/500). 🟢

---

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Criar estrutura de orquestração de agentes de IA (`app/services/agent_orchestrator.py`) | Must | Executar fluxo multiagentes recebendo input da tarefa | 🟡 |
| RF-02 | Definir schemas Pydantic v2 de saída de análise (`app/schemas/agent_output.py`) | Must | Validação estrita de tipos, campos obrigatórios e sanitização | 🟡 |
| RF-03 | Implementar Repair Loop anti-alucinação (`app/services/repair_loop.py`) | Must | Até 3 tentativas de reparo com traceback do Pydantic | 🟡 |
| RF-04 | Implementar ferramentas Python determinísticas (tools) para os agentes | Must | Cálculos numéricos delegados exclusivamente às funções Python | 🟡 |
| RF-05 | Integrar o orquestrador ao worker Celery (`app/worker.py`) e atualizar PostgreSQL | Must | Salvar status `completed` ou `failed` com resultado formatado | 🟢 |

---

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Confiabilidade | 0 falhas de schema no PostgreSQL | Validação Pydantic estrita bloqueia gravações malformadas | 🟡 |
| Resiliência | Retries automáticos com backoff exponencial | Previne falhas por instabilidade de rede ou rate limits de APIs LLM | 🟡 |
| Auditabilidade | Logs detalhados de cada iteração do Repair Loop | Permite identificar alucinações e otimizar prompts futuros | 🟢 |

---

## 7. Critérios de Aceitação

```gherkin
Cenário: Execução de agente com validação bem-sucedida de primeira
  Dado que o worker Celery recebe uma tarefa válida
  Quando o orquestrador executa a cadeia de agentes
  E a LLM devolve um JSON compatível com o schema Pydantic
  Então o resultado é validado sem erros
  E a tarefa é salva no PostgreSQL com status "completed"

Cenário: Ativação do Repair Loop com sucesso na 2ª tentativa
  Dado que a LLM retorna um JSON malformado na 1ª tentativa
  Quando o Repair Loop intercepta o ValidationError do Pydantic
  E re-envia o prompt para a LLM com a mensagem de erro explicativa
  Então a LLM corrige o JSON na 2ª tentativa
  E o resultado final é validado e persistido com sucesso

Cenário: Esgotamento das tentativas do Repair Loop
  Dado que a LLM continua retornando JSON inválido por 3 vezes consecutivas
  Quando o limite de 3 tentativas é atingido
  Então a tarefa é marcada como "failed" no PostgreSQL
  E a mensagem de erro registra "SchemaValidationError: Falha na validação do resultado após 3 tentativas"
```

---

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (Orquestrador de Agentes) | Must | Funcionalidade core de inteligência |
| RF-02 (Schemas Pydantic) | Must | Garantia de contrato estrito de dados |
| RF-03 (Repair Loop Anti-Alucinação) | Must | Mecanismo crítico de resiliência e estabilidade |
| RF-04 (Tools Determinísticas) | Should | Previne alucinações de cálculos numéricos |
| RF-05 (Integração Celery/PostgreSQL) | Must | Conecta o worker à persistência da aplicação |

---

## 9. Esclarecimentos

> Nenhuma dúvida aberta nesta sessão.

---

## 10. Lacunas

> Nenhuma lacuna pendente.

---

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-09-27 | Versão inicial gerada por `/reversa-requirements` | reversa-requirements |
