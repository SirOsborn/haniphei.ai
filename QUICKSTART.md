# Quick Start Guide - Testing All Services

This guide helps you test the complete integration locally in under 10 minutes.

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- Tesseract OCR installed (optional, for image/PDF OCR)
- Google Gemini API key (free from https://aistudio.google.com/app/apikey)

---

## Step 1: Setup AI Service (2 min)

```powershell
# Navigate to AI service
cd ai-service

# Create environment file
Copy-Item .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_key_here

# Install dependencies
pip install -r requirements.txt

# Start service
uvicorn main:app --reload --host 0.0.0.0 --port 8082
```

**Test it works**:
```powershell
# In a new terminal
curl -X POST http://localhost:8082/scan -F "text=Project has tight budget and aggressive deadline"
```

Expected response:
```json
{
  "data": [
    {"risk": "...", "category": "Financial", "context": "..."}
  ],
  "source": "llm"
}
```

✅ **AI Service is running!**

---

## Step 2: Setup Backend (2 min)

```powershell
# Navigate to backend
cd ../backend/api

# Install dependencies
pip install -r requirements.txt

# Set AI service URL (if not already in code)
$env:AI_SERVICE_URL="http://localhost:8082"

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Test it works**:
```powershell
# In a new terminal
curl http://localhost:8000/
```

Expected response:
```json
{"message": "Haniphei.ai Backend API"}
```

✅ **Backend is running!**

---

## Step 3: Setup Frontend (2 min)

```powershell
# Navigate to frontend
cd ../../frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start frontend
npm run dev
```

Open browser: http://localhost:5173

✅ **Frontend is running!**

---

## Step 4: Test End-to-End (1 min)

### Option A: Using Frontend UI
1. Go to http://localhost:5173
2. Paste text: "The project has a $5k budget and 1-week deadline"
3. Click "Analyze Risks"
4. See results!

### Option B: Using cURL (Backend → AI Service)

If backend has `/api/scan` endpoint ready:
```powershell
curl -X POST http://localhost:8000/api/scan `
  -H "Content-Type: multipart/form-data" `
  -F "text=Project budget is tight with aggressive timeline"
```

### Option C: Test AI Service Directly
```powershell
# Text analysis
curl -X POST http://localhost:8082/scan `
  -F "text=The contract has unclear payment terms and tight deadlines"

# File upload (if you have a PDF)
curl -X POST http://localhost:8082/scan `
  -F "file=@C:\path\to\document.pdf"
```

---

## Troubleshooting

### AI Service Won't Start

**Error**: `GEMINI_API_KEY not set`
- **Fix**: Edit `ai-service/.env` and add your API key

**Error**: `No module named 'google.generativeai'`
- **Fix**: `pip install google-generativeai`

**Error**: `pytesseract not found`
- **Fix**: Only needed for image OCR. Install Tesseract or ignore for text-only testing

### Backend Can't Reach AI Service

**Error**: `Connection refused`
- **Fix**: Make sure AI service is running on port 8082
- **Check**: `curl http://localhost:8082/` should return service info

### Frontend Can't Reach Backend

**Error**: `Network error` or CORS error
- **Fix**: Make sure backend has CORS middleware configured for `http://localhost:5173`
- **Check**: `curl http://localhost:8000/` should work

---

## Quick Test Script

Save as `test_integration.py`:

```python
import httpx
import asyncio

async def test_all():
    print("Testing AI Service...")
    async with httpx.AsyncClient() as client:
        # Test AI Service
        ai_response = await client.post(
            "http://localhost:8082/scan",
            data={"text": "Project has tight budget and deadline"}
        )
        print(f"AI Service: {ai_response.status_code}")
        print(ai_response.json())
        
        # Test Backend (if /api/scan exists)
        try:
            backend_response = await client.post(
                "http://localhost:8000/api/scan",
                data={"text": "Project has tight budget"}
            )
            print(f"\nBackend: {backend_response.status_code}")
            print(backend_response.json())
        except Exception as e:
            print(f"\nBackend not ready: {e}")

if __name__ == "__main__":
    asyncio.run(test_all())
```

Run: `python test_integration.py`

---

## What's Next?

Once all three services are running and communicating:

1. **Backend Team**: Implement authentication, database, proxy to AI service
2. **Frontend Team**: Build UI components, integrate with backend API
3. **AI Team**: Collect training data, periodically run `/train` endpoint

---

## Service URLs Summary

| Service | Development | Production (Example) |
|---------|-------------|----------------------|
| Frontend | http://localhost:5173 | https://your-app.vercel.app |
| Backend | http://localhost:8000 | https://your-backend.onrender.com |
| AI Service | http://localhost:8082 | https://your-ai.onrender.com |

---

## Getting API Keys

### Google Gemini (Free)
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `ai-service/.env`

### Ollama (Alternative, Completely Free)
1. Download from https://ollama.com
2. Install and run: `ollama pull llama3.1:8b`
3. In `ai-service/.env`: Set `LLM_PROVIDER=ollama`

---

## Common Questions

**Q: Do I need all three services running?**  
A: For development, yes. For testing AI service alone, just run AI service.

**Q: Can I use Ollama instead of Gemini?**  
A: Yes! Set `LLM_PROVIDER=ollama` in `.env`. Requires Ollama installed locally.

**Q: How do I deploy to production?**  
A: See `PROJECT_BLUEPRINT.md` → Deployment Guide section.

**Q: Where do I get test PDFs/documents?**  
A: Create a simple text file with "Project has tight budget and deadline" or find sample contracts online.

---

*Last Updated: December 19, 2025*
