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

## Git Workflow: Feature Branching (GitHub Flow)

For our team, we will adopt a Feature Branching (GitHub Flow) workflow. This approach emphasizes stability, collaboration, and code quality.

1.  **The `main` Branch is Sacred:**
    *   The `main` branch is the single primary branch and must always be stable and deployable.
    *   **Rule:** Direct pushes to `main` are strictly prohibited. All changes must go through a Pull Request.

2.  **Create Branches for Everything:**
    *   For any new feature, bug fix, or task, developers must create a new branch from the latest `main`.
    *   **Branch Naming Convention:** Use `[initials]/[type]/[short-description]`.
        *   `[initials]`: e.g., `sh` for Sun Heng, `rs` for Ry Satya, `ys` for Yung Sreyneang, `kr` for Kaem Sreyneath, `vr` for Virak Rangsey.
        *   `[type]`: Use `feat` for new features, `fix` for bug fixes, `docs` for documentation updates, `refactor` for refactoring.
        *   `[short-description]`: A concise, hyphen-separated description of the task.
        *   **Examples:** `sh/feat/integrate-new-risk-model`, `rs/fix/database-connection`, `ys/docs/update-ui-guide`

3.  **Develop and Commit on Your Branch:**
    *   Work on your dedicated feature branch, making small, logical commits. Your work is isolated and won't affect `main` until merged.

4.  **Open a Pull Request (PR):**
    *   Once your work on the branch is complete, stable, and tested, open a Pull Request (PR) to merge your branch into `main`.

5.  **Review and Discuss:**
    *   The PR serves as a platform for code review and discussion.
    *   **Reviewers:**
        *   **Sun Heng (Technical Lead):** Reviews most PRs, especially `ai-service` and critical `backend` changes.
        *   **Ry Satya (Backend Lead):** Reviews all `backend` PRs.
        *   **Yung Sreyneang (Frontend Lead):** Reviews all `frontend` PRs.
        *   If a change impacts multiple services (e.g., API changes affecting frontend and backend), relevant leads should co-review.

6.  **Merge into `main`:**
    *   After the PR is approved by the required reviewers and all automated checks (CI/CD, tests, linting) pass, the branch can be merged into `main`.
    *   The feature branch should then be deleted.

## Guiding Principle: The API is the Contract

The backend, AI service, and frontend teams work independently but are connected by the API. The API specification is the single source of truth, allowing for parallel development. The frontend can rely on mock data that matches the API contract, while the backend can develop the core logic independently.