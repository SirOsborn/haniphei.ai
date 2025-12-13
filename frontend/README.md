# Frontend for RiskSkanner.ai

This directory contains the frontend application, which provides the user interface for interacting with the RiskSkanner tool. It is a modern, client-side application built with React.

## Technology Stack
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **API Communication**: Axios

## Project Structure (`/src`)
- `main.jsx`: The entry point for the React application.
- `App.jsx`: The main application component.
- `index.css`: Global styles and Tailwind CSS imports.

## Folder Structure

```
frontend/
├── src/
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── README.md
├── tailwind.config.js
└── vite.config.js
```

## How to Run
1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install Dependencies**:
    This command will download all the necessary packages defined in `package.json`.
    ```bash
    npm install
    ```
3.  **Run the Development Server**:
    ```bash
    npm run dev
    ```
    The application will be available at `http://127.0.0.1:5173` (or another port if 5173 is in use).
