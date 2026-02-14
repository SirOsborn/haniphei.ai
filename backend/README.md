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
        └── storage.py    # S3/R2 storage service
```

## How to Run

1.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```

4.  **Run database migrations**:
    ```bash
    alembic upgrade head
    ```

5.  **Run the Development Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

6.  **Run tests**:
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
