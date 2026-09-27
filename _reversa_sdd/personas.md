# Personas e Jornadas

> Selo 🟡 PLANEJADO em todos os itens.

## Persona 1: Engenheiro Backend / Desenvolvedor de IA
- **Perfil:** 🟡 Desenvolvedor Backend e Engenheiro de IA focado em arquiteturas limpas e prontas para produção.
- **Contexto:** 🟡 Atua no desenvolvimento de sistemas de IA corporativos e precisa expor tarefas de longa duração de agentes de IA através de uma API HTTP sem causar timeout nem travar a requisição do cliente.
- **Nível técnico:** 🟡 Avançado em Python, FastAPI e Docker; Intermediário em Celery/Redis, PostgreSQL e validação de LLMs via Pydantic/Structured Outputs.
- **Dor principal:** 🟡 Timeouts HTTP em tarefas demoradas de agentes de IA e falhas de persistência causadas por saídas não-determinísticas de LLMs.
- **Objetivo final:** 🟡 Prover uma infraestrutura limpa, assíncrona e resiliente de automação de agentes de IA que atenda aos padrões corporativos de produção.

### Jornada principal
1. 🟡 Enviar requisição POST /tasks com o payload da tarefa e validação via Pydantic
2. 🟡 Receber resposta síncrona imediata (202 Accepted) contendo task_id e status "queued"
3. 🟡 Acompanhar a execução assíncrona do Worker Celery consumindo a fila do Redis
4. 🟡 Consultar o status e progresso da execução via GET /tasks/{task_id}
5. 🟡 Obter o resultado final estruturado e validado persistido no PostgreSQL

---
Gerado por reversa-researcher em 2026-09-27T11:37:10-03:00
Fonte: ideation.md
