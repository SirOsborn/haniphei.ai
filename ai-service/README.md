# AI Service for Haniphei.ai

This directory contains the core AI and ML components for the Haniphei.ai project. Its primary responsibility is to process incoming text or documents, perform risk analysis, and return structured data to the backend API.

## Technology Stack
- **Language**: Python 3.9+
- **Document Processing**:
  - `PyMuPDF`: For extracting text from `.pdf` files (including OCR for scanned PDFs).
  - `python-docx`: For extracting text from `.docx` files.
  - `pytesseract` + `Tesseract OCR`: OCR for images and scanned documents with **Khmer + English** bilingual support.
  - `Pillow`: Image processing for OCR.
- **AI & Machine Learning**:
  - `scikit-learn`: For building and training custom risk detection models.
  - `spacy`: For Natural Language Processing (NLP) tasks like entity recognition and text classification.
  - `pandas` & `numpy`: For data manipulation and analysis.

## Language Support
✅ **Khmer (ភាសាខ្មែរ)** - Fully supported for contracts and legal documents  
✅ **English** - Full support  
✅ **Mixed Khmer-English** - Automatically detects and processes both languages in the same document

## Structure
- `main.py`: FastAPI endpoints orchestrating OCR, LLM analysis, and local model inference.
- `ocr.py`: Utilities for extracting text from PDFs, DOCX, and images.
- `llm.py`: LLM client abstraction supporting Google Gemini and Ollama.
- `trainer.py`: Continuous training on accumulated LLM-labeled data (multi-label classifier).
- `pipeline.py`: Hybrid decision logic to choose LLM vs local model.
- `config.py`: Centralized settings, env vars, and path management.
- `requirements.txt`: Python dependencies.

## Folder Structure

```
ai-service/
├── main.py
├── ocr.py
├── llm.py
├── trainer.py
├── pipeline.py
├── config.py
├── requirements.txt
└── README.md
```

## Hybrid Approach Overview
- **Phase 1 (LLM-first)**: The service uses an LLM to extract risks from text and stores the inputs/outputs for training.
- **Phase 2 (Continuous Fine-tuning)**: The stored data trains a local multi-label classifier. Accuracy is tracked.
- **Phase 3 (Model-first)**: When accuracy meets `ACCURACY_TARGET`, disable LLM and rely on the local model.

## Configuration

### Quick Start
1. Copy `.env.example` to `.env`:
   ```bash
   cp ai-service/.env.example ai-service/.env
   ```
2. Edit `.env` and add your API key (for Gemini) or leave as-is (for Ollama)

### Environment Variables
- **`LLM_PROVIDER`** (default: `gemini`): Choose `gemini` (cloud, free) or `ollama` (local, free)

#### Gemini Settings (Recommended for Cloud)
- **`GEMINI_API_KEY`**: Get free at https://aistudio.google.com/app/apikey
- **`GEMINI_MODEL`** (default: `gemini-1.5-flash`): Fast and free
- **Free Tier**: 15 requests/min, 1,500 requests/day

#### Ollama Settings (For Local Development)
- **`OLLAMA_URL`** (default: `http://localhost:11434`)
- **`OLLAMA_MODEL`** (default: `llama3.1:8b`)
- **Setup**: Download from https://ollama.com, then `ollama pull llama3.1:8b`

#### Hybrid Controls
- **`USE_LLM`** (default: `true`): Set to `false` to use local model instead
- **`ACCURACY_TARGET`** (default: `0.85`): Threshold to consider model production-ready

#### OCR (Windows)
- **`TESSERACT_CMD`**: Optional path to `tesseract.exe` if not in PATH
- Download: https://github.com/UB-Mannheim/tesseract/wiki

## OCR Prerequisites (Windows)

### 1. Install Tesseract OCR
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR`
- Add to PATH or set `TESSERACT_CMD` in `.env`

### 2. Install Khmer Language Data (Required for Khmer contracts)
**Important:** Tesseract doesn't include Khmer support by default!

1. Download Khmer language data:
   - Go to: https://github.com/tesseract-ocr/tessdata
   - Download: `khm.traineddata`

2. Install the language file:
   - Copy `khm.traineddata` to: `C:\Program Files\Tesseract-OCR\tessdata\`

3. Verify installation:
   ```powershell
   tesseract --list-langs
   ```
   You should see both `eng` and `khm` in the output.

### 3. Configure OCR Language
In your `.env` file:
```bash
# For both Khmer and English (recommended)
TESSERACT_LANG=eng+khm

# Or English only
# TESSERACT_LANG=eng

# Or Khmer only
# TESSERACT_LANG=khm
```

## Install and Run

### 1. Install Dependencies
```bash
cd ai-service
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example config
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_key_here

# Configure Tesseract path (Windows)
# TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Enable bilingual support (default)
# TESSERACT_LANG=eng+khm
```

### 3. Start the Service
```bash
# From within ai-service directory
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8082

# Or from project root
uvicorn ai-service.main:app --reload --host 0.0.0.0 --port 8082
```

**Service will be available at:** `http://localhost:8082`

## API Endpoints

### POST /scan
Analyze document or text for project risks.

**Request (multipart/form-data):**
- `file`: Optional file upload (PDF, DOCX, or image)
- `text`: Optional string (plain text input)
- `force_llm`: Optional boolean (override USE_LLM setting)

**RDevelopment Workflow

### Phase 1: Bootstrap with LLM
1. Set `USE_LLM=true` in `.env`
2. Process documents through `/scan` endpoint
3. Training data automatically accumulates in `data/training.jsonl`

### Phase 2: Train Local Model
1. After collecting sufficient data (20+ samples recommended)
2. Call `POST /train` to train the classifier
3. Monitor `accuracy` and `f1_micro` metrics

### Phase 3: Switch to Local Model
1. Once accuracy meets `ACCURACY_TARGET` (default: 0.85)
2. Set `USE_LLM=false` to use trained model
3. Reduces API costs and improves response time

## Project Integration

This service is designed to work independently. The backend proxies requests to this service:

```
Frontend → Backend (Port 8000) → AI Service (Port 8082)
```

**Backend integration requirements:**
- Set `AI_SERVICE_URL=http://localhost:8082` in backend environment
- Forward file/text from frontend to `/scan` endpoint
- Parse and store returned risk data
- See `backend/docs/AI_SERVICE_INTEGRATION.md` for details

## Troubleshooting

### Tesseract not found
- Ensure Tesseract is installed
- Set `TESSERACT_CMD` in `.env` to full path

### Khmer characters not recognized
- Download and install `khm.traineddata` (see OCR Prerequisites above)
- Verify with: `tesseract --list-langs` (should show `khm`)
- Set `TESSERACT_LANG=eng+khm` in `.env`

### LLM returns empty risks
- Check if `GEMINI_API_KEY` is set correctly
- Verify text was extracted properly (check service logs)
- Try with `force_llm=true` parameter

### Low OCR quality
- Use high-resolution scans (300+ DPI recommended)
- Ensure good contrast between text and background
- For Khmer: Use `tessdata_best` instead of `tessdata` for better accuracy

## Additional Resources

- **Khmer OCR Setup**: See [KHMER_OCR_SETUP.md](KHMER_OCR_SETUP.md) for detailed instructions
- **Backend Integration**: See `../backend/docs/AI_SERVICE_INTEGRATION.md`
- **Project Overview**: See `../README.md`
    {
      "risk": "Budget constraints may impact delivery",
      "category": "Financial",
      "context": "Project budget is tight with no contingency mentioned"
    }
  ],
  "source": "llm"
}
```

**Risk Categories**: `Financial`, `Schedule`, `Technical`, `Legal`, `Operational`, `Compliance`, `Other`

**Example requests:**
```bash
# Text analysis (English)
curl -X POST http://localhost:8082/scan \
  -F "text=The project requires payment within 30 days with 10% penalty"

# Text analysis (Khmer)
curl -X POST http://localhost:8082/scan \
  -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ"

# File upload (PDF, DOCX, or image)
curl -X POST http://localhost:8082/scan \
  -F "file=@contract.pdf"
```

### POST /train
Train the local model from accumulated LLM-labeled data.

**Response:**
```json
{
  "accuracy": 0.87,
  "f1_micro": 0.85,
  "meets_target": true
}
```

### GET /
Service health check and configuration info.

**Response:**
```json
{
  "service": "ai-service",
  "llm_provider": "gemini",
  "use_llm": true
}
```

## Workflow Tips
- Start with `USE_LLM=true` to bootstrap training data.
- Periodically call `/train` and monitor metrics.
- Once metrics meet `ACCURACY_TARGET`, set `USE_LLM=false` to switch off LLM usage.
