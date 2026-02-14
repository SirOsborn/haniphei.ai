# Backend → AI Service Integration Spec

Requirements and contracts for backend team to integrate with AI Service.

## AI Service Connection

**URL** (development): `http://localhost:8082`  
**URL** (production): Environment variable `AI_SERVICE_URL`  
**Timeout**: Set to 60 seconds minimum (analysis can take time)

---

## API Contract: POST /scan

**Purpose**: Analyze document or text for project risks

**Request** (multipart/form-data):
- `file`: Optional file upload (PDF, DOCX, or image)
- `text`: Optional string (plain text input)
- `force_llm`: Optional boolean (override USE_LLM setting)

**Note**: Must provide at least one of `file` or `text`

**Response** (JSON):
```json
{
  "data": [
    {
      "risk": "string - short description",
      "category": "Financial|Schedule|Technical|Legal|Operational|Compliance|Other",
      "context": "string - supporting explanation"
    }
  ],
  "source": "llm" | "model"
}
```

**Risk Categories**: Financial, Schedule, Technical, Legal, Operational, Compliance, Other

---

## Integration Requirements

### 1. HTTP Client Setup
- Use HTTP client with **async support** (recommended for FastAPI)
- Set **timeout to 60+ seconds** (AI processing takes time)
- Handle file uploads and form data

### 2. Request Flow
**For file uploads**:
1. Accept file from frontend
2. Read file content
3. Forward to AI service as multipart/form-data with proper filename and content-type
4. Parse JSON response

**For text input**:
1. Accept text from frontend
2. Forward to AI service as form data
3. Parse JSON response

### 3. Error Handling
Handle these scenarios:
- **Connection Failed**: AI service not running → Return 503 Service Unavailable
- **Timeout (60s)**: Processing too long → Return 504 Gateway Timeout
- **AI Service Error**: Forward error message to frontend with appropriate status code
- **Invalid Input**: No file or text provided → Return 400 Bad Request

### 4. Response Processing
1. Extract `data` array from AI response
2. Save to database:
   - Store entire `data` array as JSON/JSONB
   - Store `source` field ('llm' or 'model')
   - Link to current user
   - Save original filename if file was uploaded
3. Return to frontend:
   - Generate `scan_id` from database
   - Include `data`, `source`, and `timestamp`

---

## Environment Variables

Add to your backend `.env`:

```bash
# AI Service connection
AI_SERVICE_URL=http://localhost:8082  # Dev
# AI_SERVICE_URL=https://your-ai-service.onrender.com  # Production
```

---

## Testing Checklist

### 1. Verify AI Service Running
```bash
curl http://localhost:8082/
# Expected: {"service": "haniphei.ai - ai service", "status": "running"}
```

### 2. Test Direct AI Service Call
```bash
# Text input
curl -X POST http://localhost:8082/scan \
  -F "text=The project budget is $10k with a 2-week deadline"

# File upload
curl -X POST http://localhost:8082/scan \
  -F "file=@./sample.pdf"
```

### 3. Test Backend Integration
```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "text=The project budget is tight"
```

### 4. Verify Complete Flow
- Login to get access token
- Call backend /scan endpoint with Authorization header
- Check response contains scan_id, data, source, timestamp
- Verify database record created with user_id

---

## Performance Tips

1. **Set Appropriate Timeout**: Use `timeout=60.0` for large PDFs
2. **Stream Large Files**: Don't load entire file into memory
3. **Add Caching**: Cache results for identical text inputs
4. **Rate Limiting**: Limit scans per user (Gemini has 1500/day free tier)

---

## Deployment Checklist

- [ ] Set `AI_SERVICE_URL` environment variable to production URL
- [ ] Configure CORS in AI Service to allow backend origin
- [ ] Test end-to-end: Frontend → Backend → AI Service
- [ ] Monitor AI Service logs for errors
- [ ] Set up health check: `GET http://ai-service/` should return 200

---

## CORS Requirements

**Backend → AI Service**: If backend and AI service are on different domains (e.g., production deployment):
- AI Service must enable CORS middleware
- Allow origins: Backend development URL (localhost:8000) and production URL
- Allow methods: POST, GET
- Allow headers: All (*)

---

## Support

- **AI Service Documentation**: See `ai-service/README.md`
- **Architecture**: See `PROJECT_BLUEPRINT.md`
- **Issues**: Tag with `@ai-service-team` in GitHub issues

---

*Last Updated: December 19, 2025*
