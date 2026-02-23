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
- `data_collector.py`: **NEW** - Enhanced data collection with metadata and features.
- `data_validator.py`: **NEW** - Data quality validation and recommendations.
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
├── data_collector.py          # NEW: Enhanced data collection
├── data_validator.py          # NEW: Data quality validation
├── requirements.txt
├── README.md
├── DATA_SCHEMA.md             # NEW: Data format documentation
├── DATA_COLLECTION_GUIDE.md   # NEW: Usage guide
└── data/
    ├── training.jsonl         # Training data (simple format)
    ├── metadata.jsonl         # Enhanced metadata & features
    └── dedup_hashes.txt       # Deduplication tracking
```

## Hybrid Approach Overview
- **Phase 1 (LLM-first)**: The service uses an LLM to extract risks from text and stores comprehensive training data with metadata.
- **Phase 2 (Continuous Fine-tuning)**: The stored data trains a local multi-label classifier with enhanced features. Accuracy is tracked.
- **Phase 3 (Model-first)**: When accuracy meets `ACCURACY_TARGET`, disable LLM and rely on the local model.

### **NEW: Enhanced Data Collection Pipeline**
The system now automatically collects comprehensive training data:
- ✅ **Automatic deduplication** - No duplicate training examples
- ✅ **Language detection** - Tracks Khmer, English, and mixed documents
- ✅ **Document classification** - Categorizes contract types automatically
- ✅ **Feature extraction** - Extracts 15+ features for better model training
- ✅ **Quality validation** - Identifies and flags low-quality samples
- ✅ **Rich metadata** - Stores document type, language, features, statistics

**See [DATA_COLLECTION_GUIDE.md](DATA_COLLECTION_GUIDE.md) for complete usage guide.**

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
Analyze document or text for project risks. **Automatically collects training data.**

**Request (multipart/form-data):**
- `file`: Optional file upload (PDF, DOCX, or image)
- `text`: Optional string (plain text input)
- `force_llm`: Optional boolean (override USE_LLM setting)

**Response:**
```json
{
  "data": [
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
curl -X POST http://localhost:8082/scan -F "text=កិច្ចសន្យានេះតម្រូវឱ្យបង់ប្រាក់ក្នុងរយៈពេល ៣០ ថ្ងៃ ដោយមានការលង្ខិតលិខិត"

# File upload (PDF, DOCX, or image)
curl -X POST http://localhost:8082/scan \
  -F "file=@contract.pdf"

#example
curl -X POST http://localhost:8082/scan -F "file=@C:\Users\PureGoat\Downloads\506594866-កុងត-រាធ-វើផ-ទះ.pdf"
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

### **NEW Data Collection Endpoints**

#### GET /data/stats
Get comprehensive statistics about collected training data.

**Response:**
```json
{
  "total_samples": 127,
  "document_types": {"construction_contract": 45, "employment_contract": 32, ...},
  "languages": {"khmer": 58, "english": 42, "mixed": 27},
  "risk_categories": {"Financial": 156, "Schedule": 98, ...},
  "avg_risks_per_doc": 3.5,
  "avg_text_length": 1456,
  "date_range": {"earliest": "...", "latest": "..."}
}
```

#### GET /data/validate
Validate dataset quality and get recommendations.

**Response:**
```json
{
  "valid": true,
  "issues": [],
  "warnings": ["2 samples have text shorter than 50 chars..."],
  "recommendations": ["READY FOR TRAINING: Dataset quality is sufficient..."]
}
```

#### GET /data/quality-issues
Identify specific low-quality samples in the dataset.

**Response:**
```json
{
  "total_issues": 3,
  "issues": [
    {
      "index": 15,
      "text_preview": "...",
      "reasons": ["Text too short", "No risks identified"]
    }
  ]
}
```

## Development Workflow

### Phase 1: Bootstrap with LLM
1. Set `USE_LLM=true` in `.env`
2. Process documents through `/scan` endpoint
3. Data automatically collected in:
   - `data/training.jsonl` (simple format)
   - `data/metadata.jsonl` (enhanced with features)
   - `data/dedup_hashes.txt` (deduplication)

### Phase 2: Monitor & Validate
1. Check collection progress: `GET /data/stats`
2. Validate quality: `GET /data/validate`
3. Review issues: `GET /data/quality-issues`
4. Aim for 50-100+ diverse samples

### Phase 3: Train Local Model
1. After collecting sufficient data (50+ samples recommended)
2. Call `POST /train` to train the classifier
3. Monitor `accuracy` and `f1_micro` metrics
4. Model now uses enhanced features for better accuracy

### Phase 4: Switch to Local Model
1. Once accuracy meets `ACCURACY_TARGET` (default: 0.85)
2. Set `USE_LLM=false` to use trained model
3. Reduces API costs to zero and improves response time
4. Continue collecting data for periodic retraining
