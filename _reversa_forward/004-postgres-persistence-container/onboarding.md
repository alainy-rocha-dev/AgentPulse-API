# Onboarding: Testando Persistência PostgreSQL e Docker Compose

## Passo a Passo de Execução

1. Copie o arquivo de exemplo de ambiente:
   ```bash
   cp .env.example .env
   ```

2. Suba toda a stack containerizada:
   ```bash
   docker-compose up --build -d
   ```

3. Verifique o status e a saúde dos 4 serviços:
   ```bash
   docker-compose ps
   ```

4. Verifique a execução das migrações Alembic no PostgreSQL:
   ```bash
   docker-compose exec web alembic current
   ```

5. Teste a persistência parando e reiniciando a stack:
   ```bash
   docker-compose down
   docker-compose up -d
   ```
