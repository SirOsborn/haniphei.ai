# Documents API - Setup & Usage Guide

## Overview

The Documents API provides secure file upload and management functionality with the following features:
- **Supported file types**: PDF, DOCX, JPG, JPEG, PNG
- **Maximum file size**: 10MB
- **Storage**: S3/Cloudflare R2
- **File path pattern**: `documents/{user_id}/{timestamp}_{filename}`
- **Cascade delete**: Deleting a document automatically deletes associated analyses
- **Authentication**: JWT-based authentication required
- **OpenAPI Documentation**: Available via Scalar UI

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/user/Documents/side-project/haniphei.ai/backend/api
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/haniphei

# JWT Secret (generate a secure random string)
JWT_SECRET=your-super-secret-key-min-32-chars-change-this

# S3/R2 Configuration
# For Cloudflare R2:
S3_ENDPOINT_URL=https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
S3_ACCESS_KEY_ID=your-r2-access-key
S3_SECRET_ACCESS_KEY=your-r2-secret-key
S3_BUCKET_NAME=haniphei-documents
S3_REGION=auto

# For AWS S3 (leave endpoint empty):
# S3_ENDPOINT_URL=
# S3_ACCESS_KEY_ID=your-aws-access-key
# S3_SECRET_ACCESS_KEY=your-aws-secret-key
# S3_BUCKET_NAME=haniphei-documents
# S3_REGION=us-east-1
```

### 3. Setup PostgreSQL Database

Install and start PostgreSQL, then create the database:

```bash
psql -U postgres
CREATE DATABASE haniphei;
\q
```

### 4. Start the API Server

```bash
uvicorn api.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### 5. Access API Documentation

- **Scalar UI**: http://localhost:8000/scalar (Modern, beautiful UI)
- **Swagger UI**: http://localhost:8000/docs (Interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (Clean documentation)

## API Endpoints

All endpoints are prefixed with `/api` as per requirements.

### Authentication Endpoints

#### 1. Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (201 Created):
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2025-12-23T10:00:00Z"
}
```

#### 2. Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get Current User
```
GET /api/auth/me
Authorization: Bearer <access_token>

Response (200 OK):
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2025-12-23T10:00:00Z"
}
```

### Document Endpoints

All document endpoints require authentication via Bearer token.

#### 1. Upload Document
```
POST /api/documents
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <binary file data>

Response (201 Created):
{
  "id": "uuid",
  "user_id": "uuid",
  "filename": "contract.pdf",
  "original_filename": "contract.pdf",
  "file_type": "application/pdf",
  "file_size": 1048576,
  "s3_key": "documents/user-id/20251223_120000_contract.pdf",
  "s3_url": "https://bucket.s3.amazonaws.com/documents/...",
  "created_at": "2025-12-23T12:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z"
}
```

**File Validation:**
- Accepted extensions: `.pdf`, `.docx`, `.jpg`, `.jpeg`, `.png`
- Accepted MIME types:
  - `application/pdf`
  - `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  - `image/jpeg`
  - `image/jpg`
  - `image/png`
- Maximum size: 10MB (10,485,760 bytes)

**Error Responses:**
- `400 Bad Request`: Invalid file type or size exceeds limit
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Upload failed (check S3/R2 configuration)

#### 2. List Documents
```
GET /api/documents?skip=0&limit=100
Authorization: Bearer <access_token>

Response (200 OK):
{
  "documents": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "filename": "contract.pdf",
      "original_filename": "contract.pdf",
      "file_type": "application/pdf",
      "file_size": 1048576,
      "s3_key": "documents/user-id/20251223_120000_contract.pdf",
      "s3_url": "https://...",
      "created_at": "2025-12-23T12:00:00Z",
      "updated_at": "2025-12-23T12:00:00Z"
    }
  ],
  "total": 1
}
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

#### 3. Get Document by ID
```
GET /api/documents/{document_id}
Authorization: Bearer <access_token>

Response (200 OK):
{
  "id": "uuid",
  "user_id": "uuid",
  "filename": "contract.pdf",
  "original_filename": "contract.pdf",
  "file_type": "application/pdf",
  "file_size": 1048576,
  "s3_key": "documents/user-id/20251223_120000_contract.pdf",
  "s3_url": "https://...",
  "created_at": "2025-12-23T12:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z",
  "analyses": [
    {
      "id": "uuid",
      "document_id": "uuid",
      "data": [...],
      "source": "llm",
      "created_at": "2025-12-23T12:05:00Z"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Document not found or doesn't belong to user

#### 4. Delete Document
```
DELETE /api/documents/{document_id}
Authorization: Bearer <access_token>

Response (204 No Content)
```

**Cascade Delete:**
- Deletes the document record from database
- Deletes the file from S3/R2 storage
- Automatically deletes all associated analyses (via database CASCADE)

**Error Responses:**
- `404 Not Found`: Document not found or doesn't belong to user
- `500 Internal Server Error`: Failed to delete from storage

## Usage Examples

### cURL Examples

#### Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepass123"}'

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepass123"}' \
  | jq -r '.access_token')
```

#### Upload Document
```bash
curl -X POST http://localhost:8000/api/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/document.pdf"
```

#### List Documents
```bash
curl -X GET http://localhost:8000/api/documents \
  -H "Authorization: Bearer $TOKEN"
```

#### Delete Document
```bash
curl -X DELETE http://localhost:8000/api/documents/{document_id} \
  -H "Authorization: Bearer $TOKEN"
```

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json={"email": "test@example.com", "password": "securepass123"}
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": "test@example.com", "password": "securepass123"}
)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Upload document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        f"{BASE_URL}/api/documents",
        headers=headers,
        files=files
    )
    document = response.json()
    print(f"Uploaded: {document['id']}")

# List documents
response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
documents = response.json()
print(f"Total documents: {documents['total']}")

# Delete document
document_id = document["id"]
response = requests.delete(
    f"{BASE_URL}/api/documents/{document_id}",
    headers=headers
)
print(f"Deleted: {response.status_code == 204}")
```

### JavaScript/TypeScript Example

```typescript
const BASE_URL = "http://localhost:8000";

// Register
const registerResponse = await fetch(`${BASE_URL}/api/auth/register`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "test@example.com",
    password: "securepass123"
  })
});

// Login
const loginResponse = await fetch(`${BASE_URL}/api/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "test@example.com",
    password: "securepass123"
  })
});
const { access_token } = await loginResponse.json();

// Upload document
const formData = new FormData();
formData.append("file", fileInput.files[0]);

const uploadResponse = await fetch(`${BASE_URL}/api/documents`, {
  method: "POST",
  headers: { "Authorization": `Bearer ${access_token}` },
  body: formData
});
const document = await uploadResponse.json();

// List documents
const listResponse = await fetch(`${BASE_URL}/api/documents`, {
  headers: { "Authorization": `Bearer ${access_token}` }
});
const { documents, total } = await listResponse.json();

// Delete document
await fetch(`${BASE_URL}/api/documents/${document.id}`, {
  method: "DELETE",
  headers: { "Authorization": `Bearer ${access_token}` }
});
```

## Project Structure

The application follows a **layered architecture** with clear separation of concerns:

```
backend/api/
├── core/                # Shared utilities
│   ├── auth.py          # JWT authentication utilities
│   ├── config.py        # Application configuration
│   └── database.py      # Database connection and session management
│
├── db/                  # Database layer
│   └── tables.py        # SQLAlchemy ORM models
│
├── models/              # Pydantic schemas (API contracts)
│   ├── auth.py          # Authentication request/response models
│   ├── document.py      # Document Pydantic schemas
│   └── risk.py          # Risk analysis Pydantic schemas
│
├── routers/             # HTTP/API layer (routes only)
│   ├── auth.py          # Authentication endpoints (HTTP layer)
│   ├── documents.py     # Document management endpoints (HTTP layer)
│   └── scan.py          # Document scanning endpoints
│
├── controllers/         # Business flow coordination
│   ├── auth.py          # Authentication business flows
│   └── document.py      # Document management business flows
│
├── services/            # Business logic layer
│   ├── auth.py          # Authentication business logic
│   ├── document.py      # Document business logic
│   └── storage.py       # S3/R2 storage service
│
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

### Architecture Layers

1. **Routes** - HTTP endpoints only, delegate to controllers
2. **Controllers** - Orchestrate business flows, handle errors
3. **Services** - Core business logic, database operations
4. **Models** - Request/response validation schemas
5. **Database** - ORM models and table definitions
6. **Core** - Shared utilities (auth, config, database)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    s3_key VARCHAR(500) NOT NULL,
    s3_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Analyses Table
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    data JSON NOT NULL,
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env` is correct
- Check database exists: `psql -U postgres -l`

### S3/R2 Upload Failures
- Verify S3/R2 credentials in `.env`
- Check bucket exists and is accessible
- For R2: Ensure endpoint URL format is correct
- Check bucket permissions allow uploads

### Authentication Errors
- Ensure JWT_SECRET is set and is at least 32 characters
- Check token is being sent in Authorization header
- Verify token hasn't expired (default: 30 minutes)

### File Upload Errors
- Check file size is under 10MB
- Verify file extension is in allowed list
- Ensure Content-Type header matches file type

## Security Considerations

1. **JWT Secret**: Use a strong, random secret key in production
2. **HTTPS**: Always use HTTPS in production to protect tokens
3. **CORS**: Configure `CORS_ORIGINS` to only include trusted domains
4. **File Validation**: Files are validated by extension and MIME type
5. **Storage**: Files are encrypted at rest (AES256) in S3/R2
6. **Database**: Use strong database credentials
7. **Rate Limiting**: Consider adding rate limiting in production

## License

This API is part of the Haniphei.ai project.
