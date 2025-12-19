# haniphei.ai

**Version**: 1.2

**Project Manager**: Rangsey VIRAK

**Technical Lead**: Heng SUN

The objective of the Haniphei.ai project is to develop a web application that automatically scans legal documents to identify, categorize, and highlight potential risks, assumptions, and dependencies, providing users with clear, structured risk reports within acceptable performance parameters.


## Project Overview

Haniphei.ai is an automated web-based platform designed to revolutionize the legal review process by reducing the manual effort required to analyze complex legal documentation.
At its core, the application serves as an intelligent risk-assessment engine. Users upload legal documents, which the system automatically parses and analyzes to detect critical risks, hidden assumptions, and operational dependencies. Rather than just displaying text, Haniphei.ai transforms unstructured legal data into a clear, interactive, and structured risk report.
The system focuses on delivering these insights within optimized performance parameters, ensuring that legal professionals and business users can assess document viability and liability in a fraction of the time required for traditional manual review.

## 📚 Documentation

### For All Teams
- **[PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)** - Complete architecture, API contracts, deployment guide
- **[QUICKSTART.md](./QUICKSTART.md)** - Test all services locally in 10 minutes

### For Specific Teams
- **[frontend/BACKEND_API_INTEGRATION.md](./frontend/BACKEND_API_INTEGRATION.md)** - Frontend team: How to integrate with backend
- **[backend/AI_SERVICE_INTEGRATION.md](./backend/AI_SERVICE_INTEGRATION.md)** - Backend team: How to integrate with AI service
- **[ai-service/README.md](./ai-service/README.md)** - AI service: Configuration, hybrid approach, OCR setup

## Architecture

The project is divided into three main components:

1.  **[Frontend](./frontend/README.md)**: React + Vite + TailwindCSS UI for document upload and risk visualization (Port: 5173)
2.  **[Backend](./backend/README.md)**: FastAPI server for authentication, database, and proxying to AI service (Port: 8000)
3.  **[AI Service](./ai-service/README.md)**: Hybrid AI engine with OCR, LLM (Gemini/Ollama), and ML model training (Port: 8082)

**Tech Highlights**:
- 🆓 **Free LLM**: Google Gemini (cloud) or Ollama (local)
- 🔄 **Hybrid AI**: Starts with LLM, transitions to local model as it learns
- 🎯 **Student-Friendly**: Deployable on free tiers (Vercel, Render, etc.)

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
# Copy and configure environment
cp .env.example .env
# Edit .env: Add GEMINI_API_KEY (get free at https://aistudio.google.com/app/apikey)
# Install dependencies
pip install -r requirements.txt
# Run service
uvicorn main:app --reload --host 0.0.0.0 --port 8082
```

**For complete setup and testing guide**, see [QUICKSTART.md](./QUICKSTART.md)

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