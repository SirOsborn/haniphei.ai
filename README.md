# haniphei.ai

**Version**: 1.2
**Project Manager**: Rangsey VIRAK
**Technical Lead**: Heng SUN

The objective of the Haniphei.ai project is to develop a web application that automatically scans legal documents to identify, categorize, and highlight potential risks, assumptions, and dependencies, providing users with clear, structured risk reports within acceptable performance parameters.


## Project Overview

Haniphei.ai is an automated web-based platform designed to revolutionize the legal review process by reducing the manual effort required to analyze complex legal documentation.
At its core, the application serves as an intelligent risk-assessment engine. Users upload legal documents, which the system automatically parses and analyzes to detect critical risks, hidden assumptions, and operational dependencies. Rather than just displaying text, Haniphei.ai transforms unstructured legal data into a clear, interactive, and structured risk report.
The system focuses on delivering these insights within optimized performance parameters, ensuring that legal professionals and business users can assess document viability and liability in a fraction of the time required for traditional manual review.

## Architecture

The project is divided into three main components:

1.  **[Frontend](./frontend/README.md)**: A React application that provides a clean and intuitive user interface for uploading files or pasting text.
2.  **[Backend](./backend/README.md)**: A FastAPI server that acts as the central API. It handles user requests and communicates with the AI service to perform the analysis.
3.  **[AI Service](./ai-service/README.md)**: A Python-based service responsible for the heavy lifting of text extraction (OCR, document parsing) and risk analysis using NLP and machine learning.

For detailed information about each component, please refer to the `README.md` file within its respective directory.

## How to Get Started

To run the entire project, you will need to start each of the three services in separate terminals.

### 1. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 2. Start the Backend API
```bash
cd backend/api
# It's recommended to use a virtual environment
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Start the AI Service
```bash
cd ai-service
# It's recommended to use a virtual environment
pip install -r requirements.txt
# (Further instructions to run as a service will be added here)
```

## Guiding Principle: The API is the Contract

The backend, AI service, and frontend teams work independently but are connected by the API. The API specification is the single source of truth, allowing for parallel development. The frontend can rely on mock data that matches the API contract, while the backend can develop the core logic independently.