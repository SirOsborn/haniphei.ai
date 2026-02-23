# Quick Start Guide - Testing All Services

This guide helps you test the complete integration locally in under 10 minutes.

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- Tesseract OCR installed (required for document OCR)
  - Download: https://github.com/UB-Mannheim/tesseract/wiki
  - **Important:** Also install Khmer language data (`khm.traineddata`) for Khmer contract support
- Google Gemini API key (free from https://aistudio.google.com/app/apikey)

---

## What You'll Get

After completing this guide:
- ✅ AI Service running with risk analysis and **automatic data collection**
- ✅ Backend fully integrated with AI service
- ✅ Frontend connected to backend
- ✅ Complete end-to-end document scanning workflow
- ✅ Training data being collected automatically for future model training

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

**Bonus - Check Data Collection**:
```powershell
# Check training data statistics
curl http://localhost:8082/data/stats

# Validate data quality
curl http://localhost:8082/data/validate
```

✅ **AI Service is running with data collection enabled!**

---

## Step 2: Setup Backend (2 min)

```powershell
# Navigate to backend
cd ../backend

# Install dependencies (includes httpx for AI service integration)
pip install -r requirements.txt

# Set AI service URL (if not already in .env)
echo "AI_SERVICE_URL=http://localhost:8082" >> .env

# Start backend (works without PostgreSQL for AI service testing)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: Backend will start without PostgreSQL for testing AI service integration. Authentication features require PostgreSQL setup (see Troubleshooting).

**Test it works**:
```powershell
# In a new terminal
curl http://localhost:8000/

# Test AI service integration (no auth required for health check)
curl http://localhost:8000/api/health
```

Expected response:
```json
{"message": "Haniphei.ai Backend API"}
```

✅ **Backend is running with AI service integration!**

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

## Step 4: Test End-to-End Integration (2 min)

### Full Integration Test (Backend → AI Service)

**Text Analysis (English)**:
```powershell
# Note: Requires authentication. Register/login first via frontend or API
curl -X POST http://localhost:8000/api/scan `
  -H "Content-Type: multipart/form-data" `
  --cookie "session=YOUR_SESSION_COOKIE" `
  -F "text=The project budget is $10,000 with payment due in 30 days. Late payment incurs 10% penalty."
```

**Text Analysis (Khmer)**:
```powershell
curl -X POST http://localhost:8000/api/scan `
  --cookie "session=YOUR_SESSION_COOKIE" `
  -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ ជាមួយនឹងការពិន័យ ១០ ភាគរយ"
```

**File Upload**:
```powershell
curl -X POST http://localhost:8000/api/scan `
  --cookie "session=YOUR_SESSION_COOKIE" `
  -F "file=@C:\path\to\contract.pdf"
```

Expected response:
```json
{
  "scan_id": null,
  "user_id": "...",
  "timestamp": "2026-02-22T10:30:00",
  "filename": "contract.pdf",
  "source": "llm",
  "risks": [
    {
      "risk": "Late payment penalties",
      "category": "Financial",
      "context": "Contract requires payment within 30 days with 10% penalty"
    }
  ],
  "risk_count": 1,
**Error**: `No module named 'scipy'`
- **Fix**: `pip install scipy` (required for enhanced model training)

### Backend Can't Reach AI Service

**Error**: `Connection refused` or `503 Service Unavailable`
- **Fix**: Make sure AI service is running on port 8082
- **Check**: `curl http://localhost:8082/` should return service info

**Error**: `httpx module not found`
- **Fix**: `pip install httpx` (required for AI service integration)

### Backend Returns 401 Unauthorized

**Error**: `401 Unauthorized` when calling `/api/scan`
- **Fix**: The endpoint requires authentication. Register/login first
- **Alternative**: Test AI service directly at `http://localhost:8082/scan` (no auth required)

### Database Connection Failed

**Error**: `password authentication failed for user "postgres"`
- **Context**: Backend can start without database for AI service testing only
- **For Full Features**: Install PostgreSQL and configure:

```powershell
# Install PostgreSQL from https://www.postgresql.org/download/windows/
# Or use Docker:
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

# Create database
# Using psql or pgAdmin, create database: haniphei

# Update backend/.env with credentials:
# DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/haniphei
```

### Frontend Can't Reach Backend

**Error**: `Network error` or CORS error
- **Fix**: Make sure backend has CORS middleware configured for `http://localhost:5173`
- **Check**: `curl http://localhost:8000/` should work
async with httpx.AsyncClient() as client:
        # Test 1: AI Service Health
        print("1. Testing AI Service Health...")
        try:
            response = await client.get("http://localhost:8082/")
            print(f"   ✅ AI Service: {response.status_code}")
            print(f"   {response.json()}")
        except Exception as e:
            print(f"   ❌ AI Service: {e}")
        
        # Test 2: AI Service Risk Analysis
        print("\n2. Testing AI Service Risk Analysis...")
        try:
            response = await client.post(
                "http://localhost:8082/scan",
                data={"text": "Project has tight budget and 2-week deadline"}
            )
            print(f"   ✅ Scan: {response.status_code}")
            result = response.json()
            print(f"   Found {len(result.get('data', []))} risks from {result.get('source')}")
        except Exception as e:
            print(f"   ❌ Scan: {e}")
        
        # Test 3: Data Collection
        print("\n3. Testing Data Collection...")
        try:
            response = await client.get("http://localhost:8082/data/stats")
            print(f"   ✅ Data Stats: {response.status_code}")
            stats = response.json()
            print(f"   Total samples collected: {stats.get('total_samples', 0)}")
        except Exception as e:
            print(f"   ❌ Data Stats: {e}")
        
        # Test 4: Backend Health
        print("\n4. Testing Backend...")
        try:
            response = await client.get("http://localhost:8000/")
            print(f"   ✅ Backend: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Backend: {e}")
        
        # Test 5: Backend AI Integration
        print("\n5. Testing Backend-AI Integration...")
        try:
            response = await client.get("http://localhost:8000/api/health")
            print(f"   ✅ Integration Health: {response.status_code}")
            print(f"   {response.json()}")
        except Exception as e:
            print(f"   ⚠️  Integration: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Haniphei.ai Integration Test")
    print("=" * 60 + "\n")
    asyncio.run(test_all())
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
```

Run: `python test_integration.py`

Expected output:
```
============================================================
Haniphei.ai Integration Test
============================================================

1. Testing AI Service Health...
   ✅ AI Service: 200
   {'service': 'ai-service', 'llm_provider': 'gemini', 'use_llm': True}

2. Testing AI Service Risk Analysis...
   ✅ Scan: 200
   Found 2 risks from llm

3. Testing Data Collection...
   ✅ Data Stats: 200
   Total samples collected: 1

4. Testing Backend...
   ✅ Backend: 200

5. Testing Backend-AI Integration...
   ✅ Integration Health: 200
   {'ai_service_healthy': True, 'status': 'ok'}

============================================================
Test Complete!
============================================================
```

✅ **All services integrated and working!**

---

## Summary

You now have:
1. ✅ **AI Service** running with Gemini LLM and automatic data collection
2. ✅ **Backend** fully integrated with AI service via httpx client
3. ✅ **Frontend** connected to backend
4. ✅ **End-to-end workflow** for document risk analysis
5. ✅ **Training data** being collected automatically for future model

**Every document you scan builds your dataset. After 100+ diverse samples, train your own model and eliminate API costs!** 🚀
   curl -X POST http://localhost:8082/train
   ```

4. **Switch to Local Model** (When accuracy ≥ 0.85)
   - Edit `ai-service/.env`: Set `USE_LLM=false`
   - Restart AI service
   - **Zero API costs from now on!**

### Learn More

- **[BACKEND_AI_INTEGRATION.md](./BACKEND_AI_INTEGRATION.md)** - Complete integration guide
- **[ai-service/DATA_COLLECTION_GUIDE.md](./ai-service/DATA_COLLECTION_GUIDE.md)** - Data collection pipeline usage
- **[ai-service/DATA_SCHEMA.md](./ai-service/DATA_SCHEMA.md)** - Training data schema
- **[PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)** - Complete architecture
### Direct AI Service Test (Bypass Backend)
```powershell
# Text analysis
curl -X POST http://localhost:8082/scan `
  -F "text=The contract has unclear payment terms and tight deadlines"

# File upload (if you have a PDF)
curl -X POST http://localhost:8082/scan `
  -F "file=@C:\path\to\document.pdf"

# Check collected training data
curl http://localhost:8082/data/stats
```

---

## Step 5: Verify Data Collection is Working (1 min)

After scanning a few documents, check that training data is being collected:

```powershell
# View statistics
curl http://localhost:8082/data/stats
```

Expected response:
```json
{
  "total_samples": 5,
  "document_types": {"construction_contract": 2, "general": 3},
  "languages": {"english": 3, "khmer": 2},
  "risk_categories": {"Financial": 8, "Schedule": 4, "Legal": 3},
  "avg_risks_per_doc": 3.0,
  "avg_text_length": 1200
}
```

Check data quality:
```powershell
curl http://localhost:8082/data/validate
```

✅ **Data collection is working! Every document scanned builds your training dataset automatically.**

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
