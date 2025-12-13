# Project Context for AI Agent (gemini.md)

## Project Name: haniphei.ai

## Mission
To create a web application that automatically scans project documents (like contracts and proposals) to identify and highlight potential risks, assumptions, and dependencies.

## Core Architecture: Decoupled Services

The project is composed of three distinct, independently deployable services:

1.  **`frontend/`**
    -   **Role**: User Interface (UI)
    -   **Tech**: React, Vite, Tailwind CSS.
    -   **Description**: This is what the user sees and interacts with. It's a client-side application that communicates with the backend via a REST API. It is responsible for file uploads, text input, and displaying the final results.

2.  **`backend/`**
    -   **Role**: API Server & Business Logic
    -   **Tech**: Python, FastAPI.
    -   **Description**: The central hub of the application. It exposes a REST API (defined in `backend/api/`) for the frontend to consume. It does **not** perform the AI analysis itself; instead, it receives requests from the frontend and calls the `ai-service` to do the actual work. Its main job is to manage HTTP traffic and coordinate between the frontend and the AI service.

3.  **`ai-service/`**
    -   **Role**: AI/ML Engine & Document Processing
    -   **Tech**: Python, PyMuPDF, `python-docx`, `scikit-learn`, `spacy`.
    -   **Description**: This is the "brain" of the project. It is responsible for all heavy processing tasks:
        -   Extracting text from `.pdf` and `.docx` files.
        -   Performing Optical Character Recognition (OCR) if needed.
        -   Running the Natural Language Processing (NLP) or Machine Learning models to identify risks in the extracted text.
    -   It is designed to be called by the `backend` service.

## Git Workflow Guidelines (Feature Branching - GitHub Flow)

To maintain code quality and facilitate collaboration, the team adheres to a Feature Branching (GitHub Flow) workflow:

1.  **`main` Branch:** Always stable and deployable. Direct pushes are prohibited.
2.  **Feature Branches:** All new work (features, bug fixes, docs) is done on dedicated branches created from `main`.
    *   **Naming Convention:** `[initials]/[type]/[short-description]` (e.g., `sh/feat/new-endpoint`).
3.  **Pull Requests (PRs):** Used to merge changes from feature branches into `main`. PRs require code review.
    *   **Reviewers:** Technical Lead (Sun Heng) for most PRs; Backend Lead (Ry Satya) for `backend` PRs; Frontend Lead (Yung Sreyneang) for `frontend` PRs. Cross-service changes require relevant lead reviews.
4.  **Merge:** Only approved PRs with passing automated checks are merged into `main`.

## Key Principle
The **API is the contract**. The `backend` defines the API, and the `frontend` consumes it. This allows for parallel development. The `ai-service` provides the core analysis functionality to the `backend`. When making changes, respect these boundaries. For example, UI changes belong in `frontend`, API endpoint changes in `backend`, and model/analysis changes in `ai-service`.
