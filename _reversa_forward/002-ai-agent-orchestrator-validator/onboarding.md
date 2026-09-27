# Onboarding: Executando e Testando o Orquestrador de IA e Repair Loop

> Feature: `002-ai-agent-orchestrator-validator`  
> Data: `2026-09-27`  

---

## 1. Pré-requisitos

1. Ambiente de desenvolvimento configurado (`Python 3.11+`).
2. Dependências instaladas (`pip install -r requirements.txt`).
3. Banco PostgreSQL e Redis em execução ou simulados via mocks nos testes.

---

## 2. Passo a Passo de Teste Automatizado

### 2.1. Executar a suíte de testes unitários do Repair Loop e Orquestrador
```bash
pytest tests/test_agent_orchestrator.py -v
```

### 2.2. O que deve ser verificado nos testes:
1. `test_successful_first_attempt`: Simula LLM retornando JSON válido de 1ª; verifica status `completed`.
2. `test_repair_loop_success_on_second_attempt`: Simula LLM retornando JSON malformado na 1ª tentativa e corrigido na 2ª; verifica se o Repair Loop corrigiu e salvou `completed`.
3. `test_repair_loop_exhaustion`: Simula 3 falhas consecutivas do LLM; verifica se a tarefa transiciona para `failed` com mensagem `"SchemaValidationError: Falha na validação do resultado após 3 tentativas"`.
4. `test_deterministic_tools`: Verifica se a função Python de cálculos estatísticos/numéricos retorna valores exatos sem alucinação.

---

## 3. Teste Fim-a-Fim no Celery Worker

1. Iniciar o Worker Celery:
   ```bash
   celery -A app.worker.celery_app worker --loglevel=info
   ```
2. Postar uma tarefa no API Gateway (`POST /api/v1/tasks`).
3. Observar nos logs do Celery a execução do `AgentOrchestrator` e a validação Pydantic.
4. Consultar o resultado via `GET /api/v1/tasks/{task_id}` e confirmar que o campo `result` contém o JSON estruturado conforme o schema.
