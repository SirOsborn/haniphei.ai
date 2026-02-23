# Backend for Haniphei.ai

This directory houses the backend web server for the project. It is built using FastAPI and serves a REST API that the frontend application consumes. Its main role is to handle HTTP requests, validate data, and communicate with the `ai-service` to get the risk analysis results.

## Technology Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Authentication**: JWT

## Architecture

The application follows a **layered architecture** with clear separation of concerns:

### Layer Breakdown

1. **Routes Layer** (`api/routers/`)
   - HTTP/API layer only
   - Defines FastAPI endpoints and OpenAPI documentation
   - Handles request/response formatting
   - Manages dependency injection (database sessions, authentication)
   - Delegates to controllers

2. **Controllers Layer** (`api/controllers/`)
   - Business flow orchestration
   - Coordinates between multiple services
   - Handles business rule validation
   - Manages HTTP exceptions and error handling
   - Transforms data between HTTP models and service models

3. **Services Layer** (`api/services/`)
   - Core business logic
   - Database operations and queries
   - External service interactions (S3, AI service)
   - Reusable business functions
   - No HTTP/framework dependencies

4. **Models Layer** (`api/models/`)
   - Pydantic schemas for API validation
   - Request/response contracts

5. **Database Layer** (`api/db/`)
   - SQLAlchemy ORM models
   - Database table definitions

6. **Core Layer** (`api/core/`)
   - Shared utilities (auth, config, database connection)
   - Cross-cutting concerns

### Benefits
- **Testability**: Each layer can be unit tested independently
- **Maintainability**: Clear responsibilities and easy to locate code
- **Reusability**: Services can be reused across multiple controllers
- **Scalability**: Easy to extend with new features
- **Separation of Concerns**: HTTP logic separate from business logic

## Project Structure

The application is organized into a modular structure for clarity and scalability:

```
backend/
├── .env.example          # Environment variables template
├── .gitignore
├── README.md
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker configuration
├── main.py               # FastAPI application entry point
├── alembic.ini           # Alembic configuration
│
├── docs/                 # Documentation
│   ├── AI_SERVICE_INTEGRATION.md
│   ├── DATABASE_IMPLEMENTATION.md
│   └── DOCUMENTS_API.md
│
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic environment config
│
├── tests/                # Test suite
│   ├── conftest.py       # Pytest configuration
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
│
└── api/                  # Main application code
    ├── core/             # Core functionality
    │   ├── auth.py       # Authentication utilities (JWT, password hashing)
    │   ├── config.py     # Application settings
    │   └── database.py   # Database connection and session management
    │
    ├── db/               # Database layer
    │   └── tables.py     # SQLAlchemy ORM models
    │
    ├── models/           # Pydantic models (API contracts)
    │   ├── auth.py       # Auth request/response models
    │   ├── document.py   # Document models
    │   └── risk.py       # Risk analysis models
    │
    ├── routers/          # HTTP/API layer (routes only)
    │   ├── auth.py       # Authentication endpoints (HTTP layer)
    │   ├── documents.py  # Document management endpoints (HTTP layer)
    │   └── scan.py       # Document scanning endpoint
    │
    ├── controllers/      # Business flow coordination
    │   ├── auth.py       # Authentication business flows
    │   └── document.py   # Document management business flows
    │
    └── services/         # Business logic layer
        ├── auth.py       # Authentication business logic
        ├── document.py   # Document business logic
        ├── storage.py    # S3/R2 storage service
        └── ai_service.py # AI service client (NEW - httpx integration)
```

## AI Service Integration

**Status**: ✅ **Fully Integrated**

The backend now has complete integration with the AI service:
- **AI Service Client** (`api/services/ai_service.py`) - Async HTTP client using httpx
- **Scan Router** (`api/routers/scan.py`) - Real integration (no longer a placeholder)
- **Error Handling** - Proper timeout, connection, and validation error handling
- **CORS Configured** - AI service accepts requests from backend

**Key Features**:
- Forward files and text to AI service for risk analysis
- Automatic data collection for model training (handled by AI service)
- Health checks and monitoring
- Support for Khmer and English documents

**See**: [BACKEND_AI_INTEGRATION.md](../BACKEND_AI_INTEGRATION.md) for complete integration guide

## How to Run

1.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install Dependencies** (includes httpx for AI service communication):
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    # Ensure AI_SERVICE_URL is set (default: http://localhost:8082)
    ```

4.  **Run database migrations**:
    ```bash
    alembic upgrade head
    ```

5.  **Start AI Service** (in separate terminal):
    ```bash
    cd ../ai-service
    python -m uvicorn main:app --reload --port 8082
    ```

6.  **Run the Development Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

7.  **Verify Integration**:
    ```bash
    # Check AI service health
    curl http://localhost:8000/api/scan/health
    ```

8.  **Run tests**:
    ```bash
    pytest
    ```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Login with email/password
- `POST /auth/logout` - Logout current session
- `GET /auth/me` - Get current user info

### Document Scanning (AI Integration)
- `POST /api/scan` - Analyze document or text for risks
  - Accepts: PDF, DOCX, images, or plain text
  - Supports: Khmer and English documents
  - Returns: Risk analysis with categories and context
- `GET /api/scan/health` - Check AI service status

### Documents (Future)
- Document management endpoints (to be implemented)

## Environment Variables

Required variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/haniphei

# Session/Auth
SESSION_SECRET_KEY=your-secret-key-min-32-characters-change-in-production

# AI Service Integration
AI_SERVICE_URL=http://localhost:8082

# File Storage (S3/R2)
S3_ENDPOINT_URL=https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=haniphei-documents
S3_REGION=auto

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## Integration Guide

### Connecting to AI Service

The backend communicates with the AI service using the `ai_service` client:

```python
from api.services.ai_service import ai_service

# In your endpoint
result = await ai_service.scan_document(
    file_content=file_bytes,
    filename="contract.pdf",
    content_type="application/pdf"
)
```

**Features:**
- Automatic timeout handling (60s for scans)
- Connection error handling
- Proper error messages for users
- Health checks

**See**: [BACKEND_AI_INTEGRATION.md](../BACKEND_AI_INTEGRATION.md) for complete guide

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=api --cov-report=html
```

Run specific test file:
```bash
pytest tests/unit/test_auth.py
```

## Development Tips

1. **Code Organization**: Follow the layered architecture strictly
2. **Error Handling**: Use HTTPException with appropriate status codes
3. **Logging**: Use Python's logging module to log important events
4. **Type Hints**: Use type hints for better IDE support and documentation
5. **Async/Await**: Use async functions for database and external service calls
6. **Testing**: Write tests for all business logic in services layer

## Additional Resources

- **[PROJECT_BLUEPRINT.md](../PROJECT_BLUEPRINT.md)** - Complete architecture
- **[BACKEND_AI_INTEGRATION.md](../BACKEND_AI_INTEGRATION.md)** - AI service integration guide
- **[docs/DATABASE_IMPLEMENTATION.md](./docs/DATABASE_IMPLEMENTATION.md)** - Database schema
- **[docs/AI_SERVICE_INTEGRATION.md](./docs/AI_SERVICE_INTEGRATION.md)** - Legacy integration spec
