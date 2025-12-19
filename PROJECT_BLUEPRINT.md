# Haniphei.ai - Project Blueprint & Architecture

**Version**: 1.0  
**Date**: December 19, 2025  
**Purpose**: Central documentation for Frontend, Backend, and AI Service integration

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Service Responsibilities](#service-responsibilities)
4. [API Contracts](#api-contracts)
5. [Development Setup](#development-setup)
6. [Deployment Guide](#deployment-guide)
7. [Team Workflows](#team-workflows)

---

## Overview

Haniphei.ai is a hybrid AI-powered risk analysis platform that:
- Accepts documents (PDF, DOCX, images) or text input
- Extracts and analyzes content using OCR and LLM
- Identifies project risks across multiple categories
- Continuously improves through fine-tuning a local model
- Transitions from LLM to local model as accuracy improves

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│              (React + Vite + TailwindCSS)                   │
│                    Port: 5173 (dev)                         │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP Requests
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND API                            │
│                  (FastAPI + Python)                         │
│                    Port: 8000 (dev)                         │
│                                                             │
│  Responsibilities:                                          │
│  • User authentication & sessions                           │
│  • Request validation & rate limiting                       │
│  • Data persistence (users, scans, history)                 │
│  • Proxies requests to AI Service                           │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP Requests
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                      AI SERVICE                             │
│              (FastAPI + ML/OCR/LLM)                         │
│                    Port: 8082 (dev)                         │
│                                                             │
│  Responsibilities:                                          │
│  • OCR extraction (PDF, DOCX, images)                       │
│  • LLM risk analysis (Gemini or Ollama)                     │
│  • Training data collection                                 │
│  • Local model training & inference                         │
│  • Hybrid decision: LLM vs Model                            │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         ↓                                    ↓
┌──────────────────┐              ┌─────────────────────┐
│  Google Gemini   │              │   Ollama (Local)    │
│   (Cloud API)    │              │   llama3.1:8b       │
│  Free: 1500/day  │              │   Completely Free   │
└──────────────────┘              └─────────────────────┘
```

---

## Service Responsibilities

### 1. Frontend Team

**Tech Stack**: React, Vite, TailwindCSS  
**Port**: 5173 (dev), static hosting (prod)

#### Responsibilities
- Build responsive UI for document/text upload
- Display risk analysis results in cards/tables
- Show risk categories with visual indicators
- Handle loading states and errors
- Integrate with Backend API (not directly with AI Service)

#### Key Components
```
frontend/src/
├── components/
│   ├── FileUpload.jsx        # Drag & drop file upload
│   ├── TextInput.jsx          # Manual text input
│   ├── RiskCard.jsx           # Display individual risk
│   ├── RiskList.jsx           # Display all risks
│   └── LoadingSpinner.jsx     # Loading state
├── services/
│   └── api.js                 # Backend API client
└── pages/
    ├── Home.jsx               # Landing page
    └── Scan.jsx               # Main scan interface
```

#### API Integration
```javascript
// frontend/src/services/api.js
const API_BASE = 'http://localhost:8000'; // Backend API

// Submit scan request
export async function submitScan(file, text) {
  const formData = new FormData();
  if (file) formData.append('file', file);
  if (text) formData.append('text', text);
  
  const response = await fetch(`${API_BASE}/api/scan`, {
    method: 'POST',
    body: formData,
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  return response.json();
}
```

**Expected Response Format**:
```json
{
  "scan_id": "uuid-here",
  "data": [
    {
      "risk": "Budget constraints identified",
      "category": "Financial",
      "context": "The project charter mentions tight budget with no buffer."
    }
  ],
  "source": "llm",
  "timestamp": "2025-12-19T10:30:00Z"
}
```

---

### 2. Backend Team

**Tech Stack**: FastAPI, Python, PostgreSQL (or SQLite for local dev)  
**Port**: 8000 (dev)

**⚠️ IMPLEMENTATION STATUS**: Database integration not yet implemented  
**Backend team TODO**: Add SQLAlchemy, database models, authentication, and CRUD operations

#### Responsibilities
- User authentication (JWT tokens) - **TO IMPLEMENT**
- Request validation and sanitization
- Database operations (users, scans, history) - **TO IMPLEMENT**
- Proxy requests to AI Service - **PARTIALLY DONE**
- Rate limiting and caching - **TO IMPLEMENT**
- Error handling and logging

#### Key Endpoints

**Authentication**
```python
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

**Scan Operations**
```python
POST /api/scan              # Submit new scan
GET  /api/scans             # List user's scans
GET  /api/scans/{scan_id}   # Get specific scan
DELETE /api/scans/{scan_id} # Delete scan
```

#### Integration Requirements

**Proxying to AI Service**:
- Accept file/text from frontend
- Forward to AI Service at `AI_SERVICE_URL/scan`
- Set 60+ second timeout
- Handle errors (503 if AI service down, 504 if timeout)
- Parse JSON response

**Database Operations**:
- Save scan results to database with user association
- Store full risk data array as JSONB
- Save source field ('llm' or 'model')
- Save original filename if file upload
- Return scan_id to frontend

**See detailed specs**:
- Database requirements → [backend/DATABASE_IMPLEMENTATION.md](backend/DATABASE_IMPLEMENTATION.md)
- AI integration → [backend/AI_SERVICE_INTEGRATION.md](backend/AI_SERVICE_INTEGRATION.md)

---

### 3. AI Service Team

**Tech Stack**: FastAPI, scikit-learn, Google Gemini, Ollama  
**Port**: 8082 (dev)

#### Responsibilities
- OCR text extraction from documents
- LLM-based risk analysis
- Training data accumulation
- Local model training
- Hybrid routing (LLM vs Model)

#### Key Endpoints

```python
GET  /                      # Service health & config
POST /scan                  # Analyze text/file for risks
POST /train                 # Train local model from accumulated data
```

#### Configuration
See `ai-service/.env.example` for all options.

---

## API Contracts

### Frontend ↔ Backend

#### POST /api/scan
**Request** (multipart/form-data):
```
file: <File> (optional)
text: <string> (optional)
```

**Response** (200 OK):
```json
{
  "scan_id": "uuid",
  "data": [
    {
      "risk": "string",
      "category": "Financial|Schedule|Technical|Legal|Operational|Compliance|Other",
      "context": "string"
    }
  ],
  "source": "llm|model",
  "timestamp": "ISO8601"
}
```

**Error Response** (4xx/5xx):
```json
{
  "error": "Error message",
  "detail": "Additional details"
}
```

---

### Backend ↔ AI Service

#### POST /scan
**Request** (multipart/form-data):
```
file: <File> (optional)
text: <string> (optional)
force_llm: <boolean> (optional)
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "risk": "string",
      "category": "string",
      "context": "string"
    }
  ],
  "source": "llm|model"
}
```

#### POST /train
**Request**: Empty body

**Response** (200 OK):
```json
{
  "accuracy": 0.87,
  "f1_micro": 0.85,
  "meets_target": true
}
```

---

## Development Setup

### Prerequisites
- **Node.js** 18+ (Frontend)
- **Python** 3.9+ (Backend & AI Service)
- **Tesseract OCR** (for AI Service image processing)
- **Ollama** (optional, for local LLM)

### Quick Start (All Services)

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/haniphei.ai.git
cd haniphei.ai
```

#### 2. Setup AI Service
```bash
cd ai-service
cp .env.example .env
# Edit .env: Add GEMINI_API_KEY from https://aistudio.google.com/app/apikey
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8082
```

#### 3. Setup Backend
```bash
cd ../backend/api

# Install dependencies (add database packages first - see Backend Team section)
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env: Add DATABASE_URL, JWT_SECRET

# Run database migrations (once implemented)
alembic upgrade head

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**⚠️ NOTE**: Database integration not yet implemented. Backend team needs to add SQLAlchemy setup first.

#### 4. Setup Frontend
```bash
cd ../../frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

### Testing Integration

**Test AI Service Directly**:
```bash
curl -X POST http://localhost:8082/scan \
  -F "text=The project has a tight budget and aggressive deadline"
```

**Test Backend → AI Service**:
```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "text=The project has a tight budget"
```

---

## Deployment Guide

### Recommended Stack (Free Tier)

**Frontend**: Vercel or Netlify  
**Backend**: Render (750 hrs/month free)  
**AI Service**: Render (750 hrs/month free)  
**Database**: Render PostgreSQL (free tier) or Supabase (500MB free)

**Local Development Database Options**:
- **PostgreSQL** (recommended): Install locally or use Docker
- **SQLite**: Quick for testing, but PostgreSQL recommended for prod compatibility

### Environment Variables

#### AI Service (Render)
```
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_key
USE_LLM=true
ACCURACY_TARGET=0.85
```

#### Backend (Render)
```
# AI Service
AI_SERVICE_URL=https://your-ai-service.onrender.com

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/haniphei_db
# For local: postgresql+asyncpg://postgres:password@localhost:5432/haniphei_dev

# Authentication
JWT_SECRET=your_random_secret_here_min_32_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
```

#### Frontend (Vercel)
```
VITE_API_URL=https://your-backend.onrender.com
```

### Deployment Steps

1. **Deploy AI Service First**
   - Push to GitHub
   - Connect to Render
   - Add environment variables
   - Note the service URL

2. **Deploy Backend**
   - Add AI_SERVICE_URL pointing to step 1
   - Deploy to Render
   - Note the service URL

3. **Deploy Frontend**
   - Add VITE_API_URL pointing to step 2
   - Deploy to Vercel
   - Done!

---

## Team Workflows

### Sprint Planning

**Week 1-2: Foundation**
- Frontend: Build upload UI components
- Backend: Setup auth & database
- AI Service: Test Gemini integration, verify OCR

**Week 3-4: Integration**
- Frontend: Connect to backend API
- Backend: Proxy scan requests to AI Service
- AI Service: Collect training data from real usage

**Week 5-6: Enhancement**
- Frontend: Add scan history, improve UX
- Backend: Add caching, rate limiting
- AI Service: Train local model, evaluate metrics

**Week 7-8: Optimization**
- Frontend: Performance optimization
- Backend: Load testing
- AI Service: Switch to local model if accuracy > 0.85

---

## Troubleshooting

### Frontend Issues

**CORS Errors**:
- Backend must add CORS middleware for frontend origin
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### Backend Issues

**AI Service Connection Timeout**:
- Increase httpx timeout: `timeout=60.0`
- Check AI_SERVICE_URL is correct
- Verify AI Service is running

### AI Service Issues

**Gemini API Errors**:
- Check GEMINI_API_KEY is set
- Verify not exceeding free tier (1500/day)
- Check API status: https://status.cloud.google.com

**OCR Not Working**:
- Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Set TESSERACT_CMD in .env

---

## FAQ

**Q: Can we use OpenAI instead of Gemini?**  
A: Not recommended for students (costs money). Stick with Gemini (free) or Ollama (local).

**Q: How do we train the local model?**  
A: Use real data! Each scan via Gemini is logged. Once you have ~500+ samples, call `POST /train`.

**Q: When should we switch from LLM to local model?**  
A: When `/train` returns `meets_target: true` (accuracy ≥ 0.85), set `USE_LLM=false`.

**Q: Can we run everything locally?**  
A: Yes! Use `LLM_PROVIDER=ollama` and run `ollama pull llama3.1:8b`.

---

## Contact & Support

**Project Manager**: [Virak Rangsey / virakrangsey@gmail.com]

**Repository**: https://github.com/SirOsborn/haniphei.ai
**Issues**: https://github.com/yourusername/haniphei.ai/issues

---

*Last Updated: December 19, 2025*
