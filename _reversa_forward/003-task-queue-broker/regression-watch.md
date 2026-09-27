# Regression Watch: Fila de Tarefas e Mensageria (`task-queue-broker`)

> Identificador: `003-task-queue-broker`  
> Data: `2026-09-27`  
> Âncora: Greenfield (`prd.md` + specs SDD)

## Tabela de Verificação

| ID | Origem (arquivo, seção) | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|-------------------------|-----------------------------|---------------------|-------------------|

## Histórico de re-extrações

*(Vazio - será preenchido nas próximas re-extrações do `/reversa`)*

## Arquivadas

*(Nenhuma)*

## Observações

- **RF-003-01**: Celery app configurado com `acks_late=True` e `task_time_limit=300`.
- **RF-003-02**: Worker Celery atualiza status no banco para `running` ao iniciar o processamento da tarefa.
- **RF-003-03**: Retentativas exponenciais (`tenacity`) aplicadas nas gravações síncronas do PostgreSQL dentro do Worker.
- **RF-003-04**: Logs detalhados emitidos no worker para rastrear o consumo e conclusão de mensagens.
