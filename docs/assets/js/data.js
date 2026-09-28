window.RV_DATA = {
  projectName: "API de Automação de Agentes de IA",
  version: "1.0.0",
  config: {
    visualStyle: "premium",
    readerProfile: "novo_dev",
    depth: "full"
  },
  seedShort: "7a8b9c0d",
  sealSvg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%"><rect width="800" height="800" rx="40" fill="#090d16"/><polygon points="400,160 590,270 590,490 400,600 210,490 210,270" fill="none" stroke="#8b5cf6" stroke-width="6"/><circle cx="400" cy="400" r="80" fill="#0f172a" stroke="#ec4899" stroke-width="6"/><text x="400" y="412" font-family="sans-serif" font-size="36" font-weight="900" fill="#ffffff" text-anchor="middle">AGENTPULSE API</text></svg>`,
  sealMiniSvg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="32" height="32"><rect width="64" height="64" rx="16" fill="#0f172a"/><polygon points="32,8 52,20 52,44 32,56 12,44 12,20" fill="none" stroke="#6366f1" stroke-width="4"/><circle cx="32" cy="32" r="8" fill="#6366f1"/></svg>`,
  nav: [
    {"id": "index", "href": "index.html", "label": "Visão Geral"},
    {"id": "arquitetura", "href": "arquitetura.html", "label": "Arquitetura 3D"},
    {"id": "modulos", "href": "modulos.html", "label": "Mapa de Módulos"},
    {"id": "metricas", "href": "metricas.html", "label": "Métricas & Cobertura"},
    {"id": "glossario", "href": "glossario.html", "label": "Glossário"},
    {"id": "f001", "href": "features/001-api-gateway-task-management.html", "label": "F001: API Gateway"},
    {"id": "f002", "href": "features/002-ai-agent-orchestrator-validator.html", "label": "F002: AI Orchestrator"},
    {"id": "f003", "href": "features/003-task-queue-broker.html", "label": "F003: Task Queue"},
    {"id": "f004", "href": "features/004-postgres-persistence-container.html", "label": "F004: PostgreSQL & Docker"}
  ],
  modules: [
    {
      name: "app/main.py",
      type: "API Entrypoint",
      description: "Inicialização do FastAPI, CORS, middleware de limite de payload (10 MB) e roteamento de rotas v1."
    },
    {
      name: "app/api/v1/endpoints/tasks.py",
      type: "Controller",
      description: "Submissão de tarefas (POST /tasks) com HTTP 202 e consulta de status (GET /tasks/{task_id})."
    },
    {
      name: "app/services/repair_loop.py",
      type: "Orchestrator Service",
      description: "Cadeia de agentes de IA com validação de esquema Pydantic e loop de reparo anti-alucinação."
    },
    {
      name: "app/worker.py",
      type: "Celery Worker",
      description: "Processamento de tarefas assíncronas em segundo plano com transição de status e retries via Tenacity."
    },
    {
      name: "app/core/database.py & app/models/task.py",
      type: "Database Layer",
      description: "Mapeamento ORM SQLAlchemy da tabela tasks e gerenciamento de sessões assíncronas."
    },
    {
      name: "docker-compose.yml & alembic/",
      type: "Infrastructure",
      description: "Orquestração multi-container para API, Worker Celery, Redis e PostgreSQL 16 com migrações automáticas."
    }
  ],
  metrics: {
    totalFeatures: 4,
    completedFeatures: 4,
    totalActions: 36,
    unitTests: 17,
    testPassRate: "100%",
    servicesCount: 4
  }
};
