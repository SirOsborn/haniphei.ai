# Development Workflow & Integration Flow

Visual guide for team collaboration and service integration.

---

## Development Workflow (Git)

```
┌─────────────────────────────────────────────────────────────┐
│                         MAIN BRANCH                         │
│                  (Always stable & deployable)               │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ Create branch
               ├─────────────────────────────────┐
               │                                 │
               ↓                                 ↓
    ┌──────────────────────┐         ┌──────────────────────┐
    │   Feature Branch     │         │   Feature Branch     │
    │  ys/feat/upload-ui   │         │ kr/feat/auth-api     │
    └──────────┬───────────┘         └───────────┬──────────┘
               │                                 │
               │ Develop                         │ Develop
               │ Test locally                    │ Test locally
               │ Commit                          │ Commit
               ↓                                 ↓
    ┌──────────────────────┐         ┌──────────────────────┐
    │   Open Pull Request  │         │   Open Pull Request  │
    └──────────┬───────────┘         └───────────┬──────────┘
               │                                 │
               │ Code Review                     │ Code Review
               │ CI Checks                       │ CI Checks
               │ Approval                        │ Approval
               ↓                                 ↓
               └─────────────┬───────────────────┘
                             │
                             │ Merge to main
                             ↓
               ┌─────────────────────────┐
               │      MAIN BRANCH        │
               │   (Updated & deployed)  │
               └─────────────────────────┘
```

---

## Service Integration Flow

### Full Request Flow: User → Response

```
┌──────────────────────────────────────────────────────────────────┐
│  1. USER uploads PDF or pastes text                              │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  2. FRONTEND (React)                                             │
│     • Validates input                                            │
│     • Shows loading spinner                                      │
│     • POST /api/scan with FormData                               │
│     • Includes JWT token in Authorization header                 │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP Request
                            │ (file/text + token)
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  3. BACKEND (FastAPI)                                            │
│     • Validates JWT token                                        │
│     • Checks rate limits                                         │
│     • Proxies to AI Service                                      │
│     • Saves scan to database                                     │
│     • Returns scan_id + results                                  │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP Request
                            │ (file/text only)
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  4. AI SERVICE (FastAPI + ML)                                    │
│     ┌────────────────────────────────────────────────┐           │
│     │  OCR Module (ocr.py)                           │           │
│     │  • Detects file type                           │           │
│     │  • PDF → PyMuPDF extraction                    │           │
│     │  • DOCX → python-docx extraction               │           │
│     │  • Image → Tesseract OCR                       │           │
│     │  • Plain text → pass through                   │           │
│     └─────────────────┬──────────────────────────────┘           │
│                       │ Extracted text                           │
│                       ↓                                          │
│     ┌────────────────────────────────────────────────┐           │
│     │  Pipeline (pipeline.py)                        │           │
│     │  • Check if USE_LLM=true                       │           │
│     │  • Check if local model exists                 │           │
│     │  • Route to LLM or Model                       │           │
│     └─────────────────┬──────────────────────────────┘           │
│                       │                                          │
│          ┌────────────┴────────────┐                             │
│          │                         │                             │
│          ↓                         ↓                             │
│  ┌───────────────┐         ┌──────────────┐                      │
│  │ LLM Client    │         │ Local Model  │                      │
│  │ (llm.py)      │         │ (trainer.py) │                      │
│  │               │         │              │                      │
│  │ • Gemini API  │         │ • Load model │                      │
│  │ • Ollama API  │         │ • Predict    │                      │
│  │ • Parse JSON  │         │ • Return     │                      │
│  │ • Log training│         │              │                      │
│  └───────┬───────┘         └──────┬───────┘                      │
│          │                        │                              │
│          └──────────┬─────────────┘                              │
│                     │ Risk data                                  │
│                     ↓                                            │
│     ┌────────────────────────────────────────────────┐           │
│     │  Response: { data: [...], source: "llm" }      │           │
│     └────────────────────────────────────────────────┘           │
└───────────────────────────┬──────────────────────────────────────┘
                            │ JSON Response
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  5. BACKEND receives response                                    │
│     • Adds scan_id from database                                 │
│     • Adds timestamp                                             │
│     • Returns to frontend                                        │
└───────────────────────────┬──────────────────────────────────────┘
                            │ JSON Response
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  6. FRONTEND displays results                                    │
│     • Hide loading spinner                                       │
│     • Render RiskCard for each risk                              │
│     • Show category badges                                       │
│     • Display source (LLM or Model)                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## AI Service: Hybrid Learning Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: LLM-First (Initial deployment)                        │
│  USE_LLM=true, no local model exists                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
        ┌──────────────────────────────────┐
        │  User scans documents            │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  LLM analyzes & returns risks    │
        │  (Gemini or Ollama)              │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Save to training.jsonl          │
        │  {text, labels, raw_risks}       │
        └────────────┬─────────────────────┘
                     │
                     │ Repeat 500+ times
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: Training (After data collection)                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
        ┌──────────────────────────────────┐
        │  Admin calls POST /train         │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Load training.jsonl             │
        │  Split train/test (80/20)        │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Train TF-IDF + LogisticReg      │
        │  Multi-label classifier          │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Evaluate on test set            │
        │  Calculate accuracy & F1         │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Save model & metrics            │
        │  risk_model.joblib               │
        │  metrics.json                    │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Returns: {accuracy, f1_micro,   │
        │            meets_target: bool}   │
        └────────────┬─────────────────────┘
                     │
                     │ If accuracy >= 0.85
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: Model-First (Production optimization)                 │
│  Set USE_LLM=false                                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
        ┌──────────────────────────────────┐
        │  User scans documents            │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Local model predicts risks      │
        │  (Fast, free, offline)           │
        └────────────┬─────────────────────┘
                     │
                     ↓
        ┌──────────────────────────────────┐
        │  Returns structured risks        │
        │  No external API calls!          │
        └──────────────────────────────────┘
```

---

## Team Coordination: Sprint Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  WEEK 1-2: Foundation                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend Team          Backend Team           AI Team          │
│  ├─ Setup Vite         ├─ Setup FastAPI      ├─ Test Gemini     │
│  ├─ UI components      ├─ Auth endpoints     ├─ Verify OCR      │
│  ├─ Upload form        ├─ Database schema    ├─ Test pipeline   │
│  └─ Mock API calls     └─ Health checks      └─ Write docs      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  WEEK 3-4: Integration                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend Team          Backend Team           AI Team          │
│  ├─ Connect to API     ├─ Proxy to AI Svc    ├─ Monitor logs    │
│  ├─ Handle auth        ├─ Save to DB         ├─ Collect data    │
│  ├─ Display results    ├─ Error handling     ├─ Fix issues      │
│  └─ Testing            └─ Rate limiting       └─ Optimize       │
│                                                                 │
│         ↓                       ↓                      ↓        │
│    ┌────────────────────────────────────────────────────┐       │
│    │   Integration Testing: End-to-End Flow             │       │
│    └────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  WEEK 5-6: Enhancement                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend Team          Backend Team           AI Team          │
│  ├─ History view       ├─ Caching            ├─ Train model     │
│  ├─ Export PDF         ├─ Search scans       ├─ Evaluate        │
│  ├─ Dark mode          ├─ Analytics          ├─ Fine-tune       │
│  └─ UX polish          └─ Performance        └─ A/B test        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  WEEK 7-8: Production Ready                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  All Teams: Deploy, monitor, optimize, document                 │
│  • Set up CI/CD                                                 │
│  • Configure production env vars                                │
│  • Performance testing                                          │
│  • User acceptance testing                                      │
│  • Documentation updates                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Communication Flow

```
┌──────────────────────────────────────────────────────────────────┐
│  Daily Standup (15 min)                                          │
│  ────────────────────────────────────────────────────────────    │
│                                                                  │
│  Frontend: "Completed upload UI, blocked on auth endpoint"       │
│  Backend:  "Auth ready, working on scan proxy"                   │
│  AI:       "Gemini working, collecting training data"            │
│                                                                  │
│  → Action: Backend to notify when /api/scan ready                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  API Changes (24hr notice)                                       │
│  ────────────────────────────────────────────────────────────    │
│                                                                  │
│  Backend: "Adding 'confidence' field to scan response in 24hrs"  │
│                                                                  │
│  → Frontend acknowledged                                         │
│  → Update PROJECT_BLUEPRINT.md                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Blocker Resolution (Immediate)                                  │
│  ────────────────────────────────────────────────────────────    │
│                                                                  │
│  Frontend: "CORS error when calling /api/scan"                   │
│  Backend:  "Adding your origin to CORS, deploying in 5min"       │
│  Frontend: "Confirmed fixed, thanks!"                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Service Ports

| Service    | Dev Port | Prod URL Pattern          |
|------------|----------|---------------------------|
| Frontend   | 5173     | your-app.vercel.app       |
| Backend    | 8000     | your-backend.onrender.com |
| AI Service | 8082     | your-ai.onrender.com      |

---

*Last Updated: December 19, 2025*
