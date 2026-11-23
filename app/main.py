from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import contribuintes, declaracoes

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
## API de Leitura - IRP/SGP

API somente leitura para consulta de dados do **Imposto de Renda da Pessoa (IRP)** no sistema SGP.

### Autenticação
Todas as rotas requerem o cabeçalho `X-API-Key` com a chave de API configurada.

### Endpoints disponíveis
- **Contribuintes** – consulta de contribuintes cadastrados
- **Declarações** – listagem e detalhes de declarações de IRP
    """,
    openapi_tags=[
        {"name": "Status", "description": "Health check da API"},
        {"name": "Contribuintes", "description": "Consulta de contribuintes"},
        {"name": "Declarações IRP", "description": "Consulta de declarações de imposto de renda"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)

app.include_router(contribuintes.router, prefix="/api/v1")
app.include_router(declaracoes.router, prefix="/api/v1")


@app.get("/", tags=["Status"])
async def root():
    return {
        "api": settings.API_TITLE,
        "versao": settings.API_VERSION,
        "docs": "/docs",
        "status": "online",
    }


@app.get("/health", tags=["Status"])
async def health():
    return {"status": "ok", "modo": "mock" if settings.USE_MOCK_DATA else "banco_de_dados"}
