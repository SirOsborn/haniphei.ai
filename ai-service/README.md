# AI Service for Haniphei.ai

This directory contains the core AI and ML components for the Haniphei.ai project. Its primary responsibility is to process incoming text or documents, perform risk analysis, and return structured data to the backend API.

## Technology Stack
- **Language**: Python 3.9+
- **Document Processing**:
  - `PyMuPDF`: For extracting text from `.pdf` files.
  - `python-docx`: For extracting text from `.docx` files.
  - `pytesseract`: For performing Optical Character Recognition (OCR) on image-based documents.
- **AI & Machine Learning**:
  - `scikit-learn`: For building and training custom risk detection models.
  - `spacy`: For Natural Language Processing (NLP) tasks like entity recognition and text classification.
  - `pandas` & `numpy`: For data manipulation and analysis.

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
Install Tesseract OCR and add to PATH, or set `TESSERACT_CMD`:
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Example: `TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe`

## Install and Run
1. **Install Dependencies**
    ```bash
    pip install -r ai-service/requirements.txt
    ```
2. **Run the Service**
    ```bash
    uvicorn ai-service.main:app --reload --host 0.0.0.0 --port 8082
    ```

## Endpoints
- `POST /scan`:
  - Form fields: `file` (optional), `text` (optional), `force_llm` (optional bool)
  - Returns: `{ data: [...], source: "llm" | "model" }`
- `POST /train`:
  - Trains the local model from accumulated data.
  - Returns: `{ accuracy, f1_micro, meets_target }`
- `GET /`:
  - Service info and current LLM configuration.

## Workflow Tips
- Start with `USE_LLM=true` to bootstrap training data.
- Periodically call `/train` and monitor metrics.
- Once metrics meet `ACCURACY_TARGET`, set `USE_LLM=false` to switch off LLM usage.
