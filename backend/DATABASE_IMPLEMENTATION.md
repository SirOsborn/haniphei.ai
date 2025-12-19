# Backend Requirements & Integration Spec

**Status**: ⚠️ TO BE IMPLEMENTED  
**Owner**: Backend Team  
**Priority**: HIGH - Required for production

---

## Overview

The backend needs to implement database persistence, user authentication, and integrate with the AI Service. This document specifies the **requirements** and **integration contracts** - implementation approach is up to the backend team.

---

## Required Components

### 1. Database

**Type**: PostgreSQL (recommended) or SQLite for local dev  
**Connection**: Async (recommended for FastAPI performance)

**Minimum Schema Requirements**:

**Users Table**:
- `id` (UUID, primary key)
- `email` (string, unique, indexed)
- `password_hash` (string)
- `created_at`, `updated_at` (timestamps)

**Scans Table**:
- `id` (UUID, primary key)
- `user_id` (UUID, foreign key → users.id, cascading delete)
- `filename` (string, nullable)
- `data` (JSON/JSONB - stores array of risk objects)
- `source` (string: 'llm' or 'model')
- `created_at` (timestamp, indexed)

**Indexes**: 
- `users.email` (for login lookups)
- `scans.user_id` (for user's scans)
- `scans.created_at DESC` (for recent scans)

---

### 2. Authentication

**Method**: JWT tokens  
**Requirements**:
- Password hashing (bcrypt or similar)
- Token expiration (recommended: 30 minutes)
- OAuth2 password flow for login

**Endpoints to implement**:
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Return JWT token
- `GET /api/auth/me` - Get current user from token

---

### 3. CORS Configuration

**Must allow**:
- Frontend origin (e.g., `http://localhost:5173` for dev)
- Credentials (for auth tokens)
- All methods and headers

**Example origins**:
- Development: `http://localhost:5173`, `http://localhost:3000`
- Production: Your Vercel/Netlify domain

---

## AI Service Integration

### Critical: How to Call AI Service

**AI Service URL**: `http://localhost:8082` (dev) or environment variable `AI_SERVICE_URL`

**Endpoint**: `POST /scan`

**Request Format** (multipart/form-data):
```
file: <UploadFile> (optional)
text: <string> (optional)
force_llm: <boolean> (optional)
```

**Response Format**:
```json
{
  "data": [
    {
      "risk": "string",
      "category": "string", 
      "context": "string"
    }
  ],
  "source": "llm" | "model"
}
```

**Implementation Requirements**:
1. Use HTTP client with 60-second timeout (AI processing can be slow)
2. Forward file/text from frontend to AI service
3. Parse JSON response from AI service
4. Save `data` array to database as JSON
5. Return scan_id, data, source, and timestamp to frontend

**Error Handling**:
- Connection timeout → 503 Service Unavailable
- AI service errors → Forward error message to frontend
- Invalid input → 400 Bad Request

---

## Required API Endpoints

Backend team must implement these endpoints:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login, return JWT
- `GET /api/auth/me` - Get current user (requires auth)

### Scan Operations
- `POST /api/scan` - Submit scan, proxy to AI service, save to DB (requires auth)
- `GET /api/scans` - List user's scans with pagination (requires auth)
- `GET /api/scans/{scan_id}` - Get specific scan (requires auth, user ownership check)
- `DELETE /api/scans/{scan_id}` - Delete scan (requires auth, user ownership check)

### Response Formats

See [PROJECT_BLUEPRINT.md](../PROJECT_BLUEPRINT.md) section "API Contracts" for complete request/response specifications.

---

## Environment Variables

Backend needs these configured:

```bash
# Required
DATABASE_URL=postgresql://...     # Or your DB connection string
JWT_SECRET=random-secret-min-32-chars
AI_SERVICE_URL=http://localhost:8082

# Optional
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,https://your-frontend.com
```

---

## Dependencies Suggestions

**Minimum required capabilities**:
- HTTP client (for calling AI service) - e.g., `httpx`, `requests`
- Database ORM/query builder - e.g., `sqlalchemy`, `prisma`, `tortoise-orm`
- JWT handling - e.g., `python-jose`, `pyjwt`
- Password hashing - e.g., `passlib`, `bcrypt`
- File upload handling - `python-multipart`

**Note**: Implementation choice is yours. Above are common libraries but not required.

---

## Testing Integration

Once implemented, test the full flow:

1. **Start AI Service** on port 8082
2. **Start Backend** on port 8000
3. **Test auth flow**:
   ```bash
   # Register
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test123"}'
   
   # Login (save the token)
   curl -X POST http://localhost:8000/api/auth/login \
     -d "username=test@test.com&password=test123"
   ```

4. **Test scan flow** (use token from step 3):
   ```bash
   curl -X POST http://localhost:8000/api/scan \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -F "text=Project has tight budget and aggressive deadline"
   ```

5. **Verify**:
   - Response includes `scan_id`, `data` array, `source`, `timestamp`
   - Data is saved in database
   - Can retrieve scan via `GET /api/scans/{scan_id}`

---

## Implementation Checklist

- [ ] Database connection configured
- [ ] User model with password hashing
- [ ] Scan model with JSON field for risks
- [ ] JWT authentication working
- [ ] CORS configured for frontend
- [ ] All 7 endpoints implemented (3 auth + 4 scan)
- [ ] AI Service integration with proper timeout
- [ ] Error handling for AI service failures
- [ ] User ownership checks on scans
- [ ] Tested end-to-end with AI service

---

## Reference Documents

- **Complete API contracts**: [PROJECT_BLUEPRINT.md](../PROJECT_BLUEPRINT.md)
- **AI Service details**: [../ai-service/README.md](../ai-service/README.md)
- **Frontend integration**: [AI_SERVICE_INTEGRATION.md](./AI_SERVICE_INTEGRATION.md)

**Questions?** Contact the AI service team or refer to documentation above.
