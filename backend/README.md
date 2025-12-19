# Backend for Haniphei.ai

This directory houses the backend web server for the project. It is built using FastAPI and serves a REST API that the frontend application consumes. Its main role is to handle HTTP requests, validate data, and communicate with the `ai-service` to get the risk analysis results.

## Technology Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Server**: Uvicorn

## Project Structure (`/api`)

The application is organized into a modular structure for clarity and scalability:

```
backend/
└── api/
    ├── main.py             # Main FastAPI app setup
    ├── requirements.txt
    ├── routers/            # To organize your API endpoints
    │   ├── __init__.py
    │   └── scan.py         # Specifically for the /scan endpoint
    ├── models/             # For Pydantic data models
    │   ├── __init__.py
    │   └── risk.py         # For the risk data structure
    └── core/               # For configuration and settings
        ├── __init__.py
        └── config.py
```

## How to Run
1.  **Navigate to the API directory**:
    ```bash
    cd backend/api
    ```
2.  **Install Dependencies**:
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Development Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.
