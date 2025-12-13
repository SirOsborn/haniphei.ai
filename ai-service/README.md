# AI Service for RiskSkanner.ai

This directory contains the core AI and ML components for the RiskSkanner.ai project. Its primary responsibility is to process incoming text or documents, perform risk analysis, and return structured data to the backend API.

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
- `main.py`: The main entry point for the AI service. This file will contain the logic for orchestrating text extraction and risk analysis.
- `requirements.txt`: A list of all Python dependencies required for this service.

## Folder Structure

```
ai-service/
├── main.py
├── requirements.txt
└── README.md
```

## How to Use
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Service**:
    The AI service is designed to be called by the main backend. The specific implementation (e.g., as a separate microservice or a library) will be defined as the project evolves.
