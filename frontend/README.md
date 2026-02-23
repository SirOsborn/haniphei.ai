# Frontend for Haniphei.ai

This directory contains the frontend application, which provides the user interface for interacting with the Haniphei.ai tool. It is a modern, client-side application built with React.

## Technology Stack
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with Glassmorphism design
- **API Communication**: Axios
- **State Management**: React Hooks

## Features

✨ **Document Upload & Analysis**
- Upload PDF, DOCX, or image files (including scanned documents)
- Input plain text for quick analysis
- Support for Khmer (ភាសាខ្មែរ) and English documents
- Real-time risk analysis with AI

🎨 **Modern UI/UX**
- Glassmorphism design with gradient effects
- Responsive layouts for all screen sizes
- Interactive file upload zones
- Real-time analysis results visualization

🔐 **Authentication**
- Secure session-based authentication
- User registration and login
- Protected routes and user profiles

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── BackgroundEffects.jsx
│   │   ├── FileUploadZone.jsx
│   │   ├── Header.jsx
│   │   ├── RiskCard.jsx
│   │   └── icons/          # Icon components
│   ├── pages/              # Page components (routes)
│   │   ├── LandingPage.jsx
│   │   ├── ScanUploadPage.jsx
│   │   ├── ResultsPage.jsx
│   │   └── ProfilePage.jsx
│   ├── hooks/              # Custom React hooks
│   │   ├── useFileUpload.js
│   │   ├── useRiskAnalysis.js
│   │   └── useAppNavigation.js
│   ├── constants/          # Constants and mock data
│   ├── App.jsx             # Main app component with routing
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
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

3.  **Configure Environment** (optional):
    Create `.env` file if you need to customize the backend URL:
    ```bash
    VITE_API_BASE_URL=http://localhost:8000
    ```

4.  **Start Backend Services**:
    Ensure backend and AI service are running:
    ```bash
    # Terminal 1 - Backend
    cd ../backend
    uvicorn main:app --reload --port 8000

    # Terminal 2 - AI Service
    cd ../ai-service
    python -m uvicorn main:app --reload --port 8082
    ```

5.  **Run the Development Server**:
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`

6.  **Build for Production**:
    ```bash
    npm run build
    ```
    Production files will be in the `dist/` directory.

## Integration with Backend

The frontend communicates with the backend API at `http://localhost:8000`:

**Authentication Flow:**
```javascript
// Login
POST /auth/login
// Body: { email, password }
// Returns: Session cookie

// Get current user
GET /auth/me
// Headers: Session cookie
```

**Document Scanning Flow:**
```javascript
// Upload and scan document
POST /api/scan
// Body: FormData with file or text
// Returns: Risk analysis results

// Expected response:
{
  "scan_id": "...",
  "timestamp": "...",
  "source": "llm" | "model",
  "risks": [
    {
      "risk": "...",
      "category": "Financial|Schedule|Technical|Legal|...",
      "context": "..."
    }
  ],
  "risk_count": 3,
  "categories": ["Financial", "Legal"]
}
```

**See**: [BACKEND_API_INTEGRATION.md](./BACKEND_API_INTEGRATION.md) for complete API documentation

## Key Features Explained

### File Upload
- Drag & drop or click to upload
- Supports: PDF, DOCX, JPG, PNG
- Client-side file validation
- Progress indication during upload

### Document Analysis
1. User uploads file or enters text
2. Frontend sends to backend API
3. Backend forwards to AI service
4. AI service performs OCR (if needed) and risk analysis
5. Results displayed in structured format with categories

### Risk Visualization
- Risk cards grouped by category
- Color-coded severity indicators
- Context and supporting details
- Export and sharing capabilities (planned)

## Design System

The application follows a consistent design system:

**Colors:**
- Primary: Purple/Blue gradients
- Accent: Rose/Pink for highlights
- Background: Dark with glassmorphism effects

**Typography:**
- Headers: Bold, large sizes for hierarchy
- Body: Readable font sizes with proper contrast
- Code/Data: Monospace for technical content

**See**: [THEME_GUIDE.md](./THEME_GUIDE.md) and [GLASSMORPHISM_GUIDE.md](./GLASSMORPHISM_GUIDE.md) for detailed design documentation

## Development Tips

1. **Component Structure**: Keep components small and focused
2. **State Management**: Use React hooks for local state
3. **API Calls**: Centralize API calls in custom hooks
4. **Error Handling**: Always handle API errors gracefully
5. **Loading States**: Show loading indicators during async operations
6. **Accessibility**: Use semantic HTML and ARIA labels

## Testing

```bash
# Run tests (when implemented)
npm test

# Linting
npm run lint
```

## Deployment

**Recommended Platform**: Vercel (free tier)

```bash
# Build
npm run build

# Deploy to Vercel
vercel deploy
```

**Environment Variables for Production:**
```
VITE_API_BASE_URL=https://your-backend-url.com
```

## Additional Resources

- **[BACKEND_API_INTEGRATION.md](./BACKEND_API_INTEGRATION.md)** - Complete API integration guide
- **[THEME_GUIDE.md](./THEME_GUIDE.md)** - Design system documentation
- **[GLASSMORPHISM_GUIDE.md](./GLASSMORPHISM_GUIDE.md)** - Glassmorphism implementation guide
- **[../PROJECT_BLUEPRINT.md](../PROJECT_BLUEPRINT.md)** - Overall project architecture

## Troubleshooting

**Issue: CORS errors**
- Ensure backend CORS is configured to allow `http://localhost:5173`
- Check that both backend and AI service are running

**Issue: Cannot connect to API**
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` environment variable
- Ensure no firewall blocking connections

**Issue: File upload fails**
- Check file size (max 10MB by default)
- Verify file type is allowed (PDF, DOCX, images)
- Check backend logs for error details
