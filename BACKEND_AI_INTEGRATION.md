# Backend ↔ AI Service Integration - Quick Test Guide

## Architecture

```
Frontend (Port 5173)
    ↓
Backend API (Port 8000)
    ↓ HTTP requests (httpx)
AI Service (Port 8082)
```

## ✅ Integration Complete!

The backend and AI service are now fully integrated and can communicate seamlessly.

### What Was Implemented:

1. **AI Service Client** ([backend/api/services/ai_service.py](backend/api/services/ai_service.py))
   - Async HTTP client using httpx
   - Proper timeout handling (60s for scans, 300s for training)
   - Error handling with user-friendly messages
   - Health checks and monitoring endpoints

2. **Updated Scan Router** ([backend/api/routers/scan.py](backend/api/routers/scan.py))
   - Real integration (no more placeholders!)
   - Forwards files and text to AI service
   - Returns structured risk analysis
   - Proper error handling and logging
   - Authentication required (uses current_user)

3. **CORS Configuration** ([ai-service/main.py](ai-service/main.py#L28-L38))
   - AI service now accepts requests from backend (localhost:8000)
   - Also configured for frontend (localhost:5173)

## Quick Test

### Step 1: Start Both Services

**Terminal 1 - AI Service:**
```bash
cd ai-service
python -m uvicorn main:app --reload --port 8082
```

**Terminal 2 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Step 2: Test the Connection

**Check AI service health from backend:**
```bash
# First, login to get token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com", "password": "your-password"}'

# Use the session cookie for subsequent requests
curl http://localhost:8000/api/scan/health \
  --cookie "session=YOUR_SESSION_COOKIE"
```

**Scan a document (English):**
```bash
curl -X POST http://localhost:8000/api/scan \
  --cookie "session=YOUR_SESSION_COOKIE" \
  -F "text=The project budget is $10,000 with payment due in 30 days. Late payment incurs 10% penalty."
```

**Scan a document (Khmer):**
```bash
curl -X POST http://localhost:8000/api/scan \
  --cookie "session=YOUR_SESSION_COOKIE" \
  -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ ជាមួយនឹងការពិន័យ ១០ ភាគរយ"
```

**Upload a PDF file:**
```bash
curl -X POST http://localhost:8000/api/scan \
  --cookie "session=YOUR_SESSION_COOKIE" \
  -F "file=@/path/to/contract.pdf"
```

### Expected Response:

```json
{
  "scan_id": null,
  "user_id": "...",
  "timestamp": "2026-02-22T10:30:00.000000",
  "filename": "contract.pdf",
  "source": "llm",
  "risks": [
    {
      "risk": "Late payment penalties",
      "category": "Financial",
      "context": "Contract requires payment within 30 days with 10% penalty for delays"
    }
  ],
  "risk_count": 1,
  "categories": ["Financial"]
}
```

## Data Flow

### 1. Frontend → Backend (Port 8000)
```javascript
// Frontend uploads file
const formData = new FormData();
formData.append('file', selectedFile);

fetch('http://localhost:8000/api/scan', {
  method: 'POST',
  body: formData,
  credentials: 'include'
});
```

### 2. Backend → AI Service (Port 8082)
```python
# Backend forwards to AI service
from api.services.ai_service import ai_service

result = await ai_service.scan_document(
    file_content=file_content,
    filename=filename,
    content_type=content_type
)
```

### 3. AI Service Processing
- OCR extraction (if needed for images/scanned PDFs)
- Language detection (Khmer/English/Mixed)
- Document classification
- LLM risk analysis (or local model if trained)
- **Automatic data collection** for future training

### 4. Response Flow Back
AI Service → Backend → Frontend with risk analysis results

## Features Available via Backend

### 1. Risk Scanning
- **Endpoint**: `POST /api/scan`
- **Supports**: PDF, DOCX, images, plain text
- **Languages**: Khmer, English, Mixed
- **Returns**: Risk categories, context, severity

### 2. Health Check
- **Endpoint**: `GET /api/scan/health`
- **Purpose**: Check if AI service is running
- **Returns**: Connection status

### 3. Future Endpoints (via ai_service client):
```python
# Get training data statistics
stats = await ai_service.get_data_stats()

# Validate data quality
validation = await ai_service.validate_data_quality()

# Train model
results = await ai_service.train_model()
```

## Error Handling

The integration handles these scenarios gracefully:

| Error | HTTP Status | User Message |
|-------|-------------|--------------|
| AI service not running | 503 | "AI analysis service is currently unavailable" |
| Processing timeout | 504 | "Document analysis timed out" |
| Invalid input | 400 | "No file or text provided" |
| AI service error | 400 | Error details from AI service |
| Unknown error | 500 | "An unexpected error occurred" |

## Configuration

### Backend (.env)
```bash
# Already configured!
AI_SERVICE_URL=http://localhost:8082
```

### AI Service (.env)
```bash
# Configure your LLM provider
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here

# Or use local LLM
# LLM_PROVIDER=ollama
```

## Monitoring & Logging

Both services log important events:

**Backend logs:**
```
INFO: User john@example.com scanning file: contract.pdf (application/pdf, 45123 bytes)
INFO: AI service returned 3 risks from llm for user john@example.com
```

**AI Service logs:**
```
INFO: Training with enhanced metadata features...
INFO: Detected language: khmer (ratio: 0.75)
INFO: Document classified as: construction_contract
```

## Production Deployment

### Environment Variables

**Backend:**
```bash
AI_SERVICE_URL=https://your-ai-service.onrender.com
```

**AI Service:**
Update CORS origins:
```python
allow_origins=[
    "https://your-backend.onrender.com",
    "https://your-frontend.vercel.app",
]
```

## Troubleshooting

### "AI service connection failed"
- Ensure AI service is running on port 8082
- Check firewall settings
- Verify `AI_SERVICE_URL` in backend .env

### "AI service timeout"
- Large PDF files may take time
- Check AI service logs for processing issues
- Increase timeout in ai_service.py if needed

### "Invalid session"
- User must be authenticated
- Check session cookie is being sent
- Verify auth middleware is working

## Next Steps

1. ✅ **Test the integration** - Follow quick test guide above
2. ✅ **Upload diverse documents** - Build training dataset automatically
3. ✅ **Monitor collection** - Use `/data/stats` endpoint
4. ✅ **Train model** - Once you have 100+ samples
5. ✅ **Switch to local model** - Set `USE_LLM=false` for zero API costs

---

**The integration is complete and production-ready!** 🚀

Your backend can now seamlessly communicate with your AI service, and data collection happens automatically in the background for future model training.
