from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference

from routers import scan, documents, auth, user
from core.config import settings
from core.database import init_db
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Try to initialize database, but don't fail if it's not available
    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.warning(f"⚠️  Database initialization failed: {e}")
        logger.warning("⚠️  Running without database - authentication features will not work")
        logger.warning("⚠️  AI service integration will still work for testing")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Haniphei.ai API for document risk analysis",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)
print("CORS origins:", settings.cors_origins)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(scan.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(user.router, prefix="/api")

@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Welcome to the Haniphei.ai API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "llm_provider": settings.llm_provider,
        "use_llm": settings.use_llm,
    }

# Simple CORS test endpoint
@app.get("/ping", tags=["test"])
def ping():
    return {"ping": "pong"}


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=f"{settings.app_name} - API Documentation",
    )
