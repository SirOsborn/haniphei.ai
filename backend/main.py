from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference

from api.routers import scan, documents, auth
from api.core.config import settings
from api.core.database import init_db
from api.controllers import auth, document, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
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
    allow_origins=[
        "https://haniphei.ai",           # Your production domain
        "https://www.haniphei.ai",       # WWW subdomain
        "http://localhost:5173",         # Local development (Vite)
        "http://localhost:3000",         # Local development (React)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Only needed methods
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "User-Agent",
    ],
    max_age=600,  # Cache preflight response for 10 minutes
)

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
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=f"{settings.app_name} - API Documentation",
    )
