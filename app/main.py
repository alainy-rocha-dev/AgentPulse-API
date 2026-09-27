from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import tasks

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="API de Automação de Agentes de IA com Validação Pydantic e Execução Assíncrona via Celery + Redis + PostgreSQL."
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Validação de Limite de Payload (10 MB)
@app.middleware("http")
async def limit_payload_size_middleware(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > settings.MAX_PAYLOAD_SIZE_BYTES:
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": "O tamanho do payload excede o limite máximo permitido de 10 MB."}
                )
        except ValueError:
            pass
    return await call_next(request)

# Registrar rotas da API v1
app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])

@app.get("/", summary="Healthcheck raiz")
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
