# Frontend → Backend API Integration Spec

Requirements and API contracts for frontend team to integrate with Backend API.

## Quick Reference

**Backend API URL** (development): `http://localhost:8000`  
**Backend API URL** (production): Set via `VITE_API_URL` environment variable

---

## Authentication

### 1. Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "user_id": "uuid-here",
  "email": "user@example.com",
  "token": "jwt-token-here"
}
```

### 2. Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "token": "jwt-token-here",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com"
  }
}
```

### 3. Get Current User
```http
GET /api/auth/me
Authorization: Bearer jwt-token-here
```

**Response**:
```json
{
  "id": "uuid-here",
  "email": "user@example.com"
}
```

---

## Main Scan Endpoint

### POST /api/scan

**Purpose**: Submit document or text for risk analysis

**Request Format**:
```http
POST /api/scan
Authorization: Bearer jwt-token-here
Content-Type: multipart/form-data

file: <File> (optional)
text: <string> (optional)
```

**Important**: Send either `file` OR `text`, or both.

**Response Format**:
```json
{
  "scan_id": "uuid-scan-id",
  "data": [
    {
      "risk": "Budget constraints may impact project delivery",
      "category": "Financial",
      "context": "The project charter mentions tight budget with no contingency."
    },
    {
      "risk": "Aggressive timeline increases schedule risk",
      "category": "Schedule",
      "context": "6-month deadline for a typically 12-month project scope."
    }
  ],
  "source": "llm",
  "timestamp": "2025-12-19T10:30:00Z"
}
```

**Risk Categories**:
- Financial
- Schedule
- Technical
- Legal
- Operational
- Compliance
- Other

---

## Scan History

### GET /api/scans
Get all scans for current user

```http
GET /api/scans?limit=10&offset=0
Authorization: Bearer jwt-token-here
```

**Response**:
```json
{
  "scans": [
    {
      "scan_id": "uuid",
      "filename": "contract.pdf",
      "risk_count": 5,
      "created_at": "2025-12-19T10:30:00Z"
    }
  ],
  "total": 1
}
```

### GET /api/scans/{scan_id}
Get specific scan details

```http
GET /api/scans/uuid-scan-id
Authorization: Bearer jwt-token-here
```

**Response**:
```json
{
  "scan_id": "uuid",
  "filename": "contract.pdf",
  "data": [ /* risk objects */ ],
  "source": "llm",
  "created_at": "2025-12-19T10:30:00Z"
}
```

### DELETE /api/scans/{scan_id}
Delete a scan

```http
DELETE /api/scans/uuid-scan-id
Authorization: Bearer jwt-token-here
```

**Response**:
```json
{
  "message": "Scan deleted"
}
```

---

## Integration Requirements

### 1. HTTP Client Setup
- Use browser `fetch` or HTTP library (axios, ky, etc.)
- Store JWT token in localStorage or secure cookie
- Add `Authorization: Bearer {token}` header for authenticated requests
- Use `FormData` for file uploads (browser sets Content-Type with boundary)
- Use `application/json` for JSON payloads

### 2. Request Patterns

**For Authentication**:
- Login/Register → Store token → Include token in subsequent requests
- Check token on app load → Fetch current user
- Handle 401 errors → Clear token → Redirect to login

**For File Upload**:
- Accept file from user (input type="file")
- Create FormData object
- Append file and optional text
- POST to /api/scan with Authorization header
- Show loading state (analysis takes 5-60 seconds)
- Display results or error

**For Text Input**:
- Accept text from textarea
- Create FormData with text field
- POST to /api/scan
- Display results

### 3. Error Handling
Handle these scenarios:
- **401 Unauthorized**: Token expired → Redirect to login
- **400 Bad Request**: Invalid input → Show validation error
- **503 Service Unavailable**: Backend or AI service down → Show retry message
- **504 Gateway Timeout**: Analysis took too long → Show timeout message

### 4. Response Processing
**Scan Response**:
- Extract `scan_id` for linking to scan history
- Display `data` array as list of risk cards
- Show `source` indicator ('llm' or 'model')
- Store `timestamp` for history

**Risk Display**:
- Each risk has: `risk`, `category`, `context`
- Categories: Financial, Schedule, Technical, Legal, Operational, Compliance, Other
- Suggested: Color-code by category, show context on expand/hover

---

## Environment Setup

Create `.env` or `.env.local` file in frontend root:

```bash
# Development
VITE_API_URL=http://localhost:8000

# Production (set in Vercel/Netlify dashboard)
# VITE_API_URL=https://your-backend.onrender.com
```

Access via `import.meta.env.VITE_API_URL`

---

## File Size & Type Limits

**Recommended Client-Side Validation**:
- Max file size: 10MB
- Accepted types: `.pdf`, `.docx`, `.png`, `.jpg`, `.jpeg`
- Show user-friendly error before upload

---

## CORS Requirements

**Backend must enable CORS** to allow frontend origin:
- Development: `http://localhost:5173` (Vite default)
- Production: Your Vercel/Netlify domain
- Allow credentials for JWT in Authorization header
- Allow methods: POST, GET, DELETE
- Allow headers: Authorization, Content-Type

---

## Testing Checklist

### 1. Test Backend Connection
```bash
curl http://localhost:8000
# Expected: Backend service info
```

### 2. Test Authentication Flow
- Register new user → Receive token
- Login → Receive token
- Call /api/auth/me with token → Receive user info
- Call without token → Receive 401

### 3. Test Scan Flow
- Upload PDF → Wait for analysis → Receive risks
- Paste text → Receive risks immediately
- Upload + text → Both processed
- No file or text → Receive 400 error

### 4. Test Error Scenarios
- Invalid token → 401
- File too large → Validation error
- Backend down → Connection error
- AI service timeout → 504 error

---

## Support

- **Backend Integration Doc**: See `backend/AI_SERVICE_INTEGRATION.md`
- **Architecture**: See `PROJECT_BLUEPRINT.md`
- **Issues**: Tag with `@backend-team` in GitHub issues

---

*Last Updated: December 19, 2025*
