# Backend Architecture

## Overview

The backend follows a **layered architecture pattern** with clear separation of concerns. This design improves testability, maintainability, and scalability by organizing code into distinct layers with specific responsibilities.

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│          HTTP Request (FastAPI)             │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────▼────────┐
         │   Routes Layer  │  ← HTTP/API endpoints only
         │  (api/routers)  │
         └────────┬────────┘
                  │ delegates to
         ┌────────▼────────┐
         │ Controllers Layer│  ← Business flow orchestration
         │(api/controllers) │
         └────────┬────────┘
                  │ calls
         ┌────────▼────────┐
         │ Services Layer   │  ← Core business logic
         │ (api/services)   │
         └────────┬────────┘
                  │ uses
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌────▼────┐   ┌───▼────┐
│  DB   │   │ External│   │ Models │
│(ORM)  │   │Services │   │(Schemas)
└───────┘   └─────────┘   └────────┘
```

## Layer Responsibilities

### 1. Routes Layer (`api/routers/`)

**Purpose**: HTTP/API layer only

**Responsibilities**:
- Define FastAPI route endpoints
- Handle HTTP request/response formatting
- Manage dependency injection (DB sessions, authentication)
- Define OpenAPI documentation (summaries, descriptions)
- Delegate business logic to controllers

**What NOT to do**:
- ❌ Business logic
- ❌ Database queries
- ❌ Complex validation
- ❌ Error handling beyond HTTP errors

**Example** ([auth.py](../api/routers/auth.py)):
```python
@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await auth_controller.register(db, user_data)
```

### 2. Controllers Layer (`api/controllers/`)

**Purpose**: Business flow orchestration

**Responsibilities**:
- Coordinate multiple services
- Handle business rule validation
- Manage error handling and HTTP exceptions
- Transform data between layers
- Orchestrate complex business flows

**What NOT to do**:
- ❌ Direct database access (use services)
- ❌ HTTP-specific concerns (handled by routes)
- ❌ External service implementation details

**Example** ([auth.py](../api/controllers/auth.py)):
```python
async def register(self, db: AsyncSession, user_data: UserRegister) -> UserResponse:
    # Business rule: Check if user exists
    existing_user = await self.auth_service.get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Delegate to service
    new_user = await self.auth_service.register_user(db, user_data)

    return UserResponse.model_validate(new_user)
```

### 3. Services Layer (`api/services/`)

**Purpose**: Core business logic and data access

**Responsibilities**:
- Database operations and queries
- Business logic implementation
- External service interactions (S3, AI service)
- Reusable business functions
- Data transformations

**What NOT to do**:
- ❌ HTTP exceptions (return errors, let controllers handle)
- ❌ Direct HTTP request/response handling
- ❌ Dependency on FastAPI

**Example** ([auth.py](../api/services/auth.py)):
```python
async def register_user(self, db: AsyncSession, user_data: UserRegister) -> User:
    """Register a new user"""
    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
```

### 4. Models Layer (`api/models/`)

**Purpose**: Data validation and contracts

**Responsibilities**:
- Pydantic schemas for request/response validation
- API contracts
- Data serialization/deserialization

**Example** ([auth.py](../api/models/auth.py)):
```python
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
```

### 5. Database Layer (`api/db/`)

**Purpose**: Database table definitions

**Responsibilities**:
- SQLAlchemy ORM models
- Database relationships
- Table schemas

**Example** ([tables.py](../api/db/tables.py)):
```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
```

### 6. Core Layer (`api/core/`)

**Purpose**: Shared utilities and cross-cutting concerns

**Responsibilities**:
- Authentication utilities (JWT, password hashing)
- Configuration management
- Database connection and session management
- Shared helpers

## Data Flow Example

Let's trace a user registration request through the layers:

```
1. HTTP POST /api/auth/register
   ↓
2. Routes Layer (api/routers/auth.py)
   - Validates request against UserRegister model
   - Injects database session
   - Calls: auth_controller.register(db, user_data)
   ↓
3. Controllers Layer (api/controllers/auth.py)
   - Checks if email already exists (calls service)
   - If exists, raises HTTPException
   - If not, calls: auth_service.register_user(db, user_data)
   ↓
4. Services Layer (api/services/auth.py)
   - Hashes password
   - Creates User ORM model
   - Saves to database
   - Returns User object
   ↓
5. Controllers Layer
   - Converts User to UserResponse (Pydantic)
   - Returns to route
   ↓
6. Routes Layer
   - FastAPI serializes UserResponse to JSON
   - Returns HTTP 201 Created
```

## Benefits of This Architecture

### 1. Testability
- **Unit tests**: Services can be tested without HTTP layer
- **Integration tests**: Controllers can be tested with mocked services
- **API tests**: Routes can be tested with real controllers

### 2. Maintainability
- Clear responsibilities for each layer
- Easy to locate code (business logic in services, HTTP in routes)
- Changes to one layer don't affect others

### 3. Reusability
- Services can be reused across multiple controllers
- Controllers can be reused across multiple routes
- Business logic is not tied to HTTP

### 4. Scalability
- Easy to add new features following the same pattern
- Can add caching, logging, or monitoring at specific layers
- Can replace implementations without changing interfaces

### 5. Separation of Concerns
- HTTP logic is separate from business logic
- Database access is isolated to services
- Easy to switch databases or ORMs

## Design Patterns Used

### 1. Layered Architecture
Organizes code into horizontal layers with clear dependencies.

### 2. Dependency Injection
FastAPI's `Depends()` injects database sessions and authentication.

### 3. Service Pattern
Encapsulates business logic in reusable service classes.

### 4. Repository Pattern (implicit)
Services act as repositories for data access.

### 5. Single Responsibility Principle
Each layer/class has one reason to change.

## Comparison: Before vs After

### Before Refactoring
```python
# Everything in the route - 80 lines
@router.post("/register")
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Create user
    new_user = User(email=user_data.email, password_hash=hashed_password)

    # Save to DB
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserResponse.model_validate(new_user)
```

### After Refactoring

**Route** (10 lines):
```python
@router.post("/register")
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await auth_controller.register(db, user_data)
```

**Controller** (15 lines):
```python
async def register(self, db: AsyncSession, user_data: UserRegister) -> UserResponse:
    existing_user = await self.auth_service.get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = await self.auth_service.register_user(db, user_data)
    return UserResponse.model_validate(new_user)
```

**Service** (12 lines):
```python
async def register_user(self, db: AsyncSession, user_data: UserRegister) -> User:
    hashed_password = get_password_hash(user_data.password)

    new_user = User(email=user_data.email, password_hash=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
```

### Improvements
- ✅ Routes are clean and focused (80 → 10 lines)
- ✅ Business logic is testable without HTTP
- ✅ Services are reusable
- ✅ Clear separation of concerns
- ✅ Easy to add features (e.g., email verification, logging)

## Adding New Features

To add a new feature, follow this pattern:

### 1. Define Models
Create Pydantic schemas in `api/models/`

### 2. Create Service
Implement business logic in `api/services/`
```python
class FeatureService:
    async def do_something(self, db: AsyncSession, data: InputModel) -> OutputModel:
        # Business logic here
        pass
```

### 3. Create Controller
Orchestrate flows in `api/controllers/`
```python
class FeatureController:
    def __init__(self):
        self.service = feature_service

    async def handle_request(self, db: AsyncSession, data: InputModel):
        # Validate, call service, handle errors
        pass
```

### 4. Create Routes
Define endpoints in `api/routers/`
```python
@router.post("/feature")
async def create_feature(
    data: InputModel,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await feature_controller.handle_request(db, data)
```

## File Organization

```
api/
├── routers/         # One file per resource (auth, documents, etc.)
├── controllers/     # One file per resource (auth, document, etc.)
├── services/        # One file per domain (auth, document, storage, etc.)
├── models/          # One file per domain (auth, document, etc.)
├── db/              # Database models (tables.py)
└── core/            # Shared utilities (auth.py, config.py, database.py)
```

## Best Practices

### Routes
- Keep routes thin (1-5 lines)
- Only handle HTTP concerns
- Delegate to controllers
- Use dependency injection

### Controllers
- Focus on business flow
- Raise HTTP exceptions
- Don't access database directly
- Call services for data access

### Services
- Pure business logic
- No HTTP dependencies
- Return data or raise ValueError
- Reusable across controllers

### Models
- Use Pydantic for validation
- Define clear request/response contracts
- Separate from ORM models

## Testing Strategy

### Unit Tests
```python
# Test services without HTTP
async def test_register_user():
    user = await auth_service.register_user(db, user_data)
    assert user.email == user_data.email
```

### Integration Tests
```python
# Test controllers with mocked services
async def test_register_controller():
    with patch('auth_service.get_user_by_email', return_value=None):
        response = await auth_controller.register(db, user_data)
        assert response.email == user_data.email
```

### API Tests
```python
# Test routes end-to-end
async def test_register_endpoint(client):
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
```

## Summary

This layered architecture provides:
- ✅ Clear separation of concerns
- ✅ Improved testability
- ✅ Better maintainability
- ✅ Enhanced reusability
- ✅ Easier to scale

Each layer has a specific purpose, and dependencies flow in one direction (routes → controllers → services → database), making the codebase easier to understand, test, and maintain.
