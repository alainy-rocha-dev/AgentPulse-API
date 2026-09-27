# Delta no Modelo de Dados: `task-queue-broker`

> Feature: `003-task-queue-broker`  
> Data: `2026-09-27`  

---

## 1. Mapeamento de Estados da Tarefa

A tabela de tarefas no PostgreSQL mantém a seguinte máquina de estados durante o ciclo de vida gerenciado pelo Celery Worker:

```
[ pending ]  --(Worker consome job)-->  [ running ]
     |                                      |
     +--(Conclusão bem-sucedida)-----------> [ completed ]
     |                                      |
     +--(Erro/Timeout/Crash)--------------> [ failed ]
```

## 2. Diffs Conceituais do Banco de Dados

- **Nenhum novo campo ou tabela física adicionada nesta feature.**
- **Atualização de Valores em Colunas Existentes:**
  - Coluna `status`: Atualizada transacionalmente pelo worker (`pending` -> `running` -> `completed` / `failed`).
  - Coluna `error_message`: Preenchida quando a tarefa transiciona para `failed`.
  - Coluna `updated_at`: Atualizada no timestamp de cada transição.
