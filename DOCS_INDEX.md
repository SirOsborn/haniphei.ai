# 📋 Documentation Index

Complete guide to all documentation for the Haniphei.ai project.

---

## 🚀 Getting Started

**New to the project? Start here:**

1. **[README.md](./README.md)** - Project overview and quick setup
2. **[QUICKSTART.md](./QUICKSTART.md)** - Test all services locally in 10 minutes
3. **[PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)** - Complete architecture and integration guide

---

## 👥 Team-Specific Guides

### For Frontend Team
- **[frontend/BACKEND_API_INTEGRATION.md](./frontend/BACKEND_API_INTEGRATION.md)**
  - How to call backend API endpoints
  - Request/response formats
  - React component examples
  - Error handling patterns

### For Backend Team
- **[backend/AI_SERVICE_INTEGRATION.md](./backend/AI_SERVICE_INTEGRATION.md)**
  - How to integrate with AI service
  - Proxy implementation examples
  - Database schema suggestions
  - Error handling and timeouts

### For AI Service Team
- **[ai-service/README.md](./ai-service/README.md)**
  - Configuration and environment setup
  - Hybrid AI architecture explained
  - OCR setup and troubleshooting
  - Endpoints documentation

---

## 📖 Comprehensive Guides

### Architecture & Design
- **[PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)**
  - System architecture diagram
  - Service responsibilities
  - API contracts (all endpoints)
  - Deployment guide (free tier options)
  - FAQ and troubleshooting

### Development Workflow
- **[WORKFLOW.md](./WORKFLOW.md)**
  - Git branching strategy
  - Service integration flow diagrams
  - Hybrid AI learning phases
  - Sprint planning templates
  - Team communication protocols

---

## 🔧 Technical References

### Configuration Files
- **[ai-service/.env.example](./ai-service/.env.example)** - AI service environment variables (with comments)
- **[.gitignore](./.gitignore)** - Git ignore patterns (includes .env, data, models)

### API Endpoints Quick Reference

**Frontend → Backend**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/scan` - Submit scan
- `GET /api/scans` - List user scans
- `GET /api/scans/{id}` - Get scan details
- `DELETE /api/scans/{id}` - Delete scan

**Backend → AI Service**
- `GET /` - Service health check
- `POST /scan` - Analyze text/document
- `POST /train` - Train local model

---

## 📚 Learning Path by Role

### Frontend Developer Path
1. Read [README.md](./README.md) - Understand project
2. Read [QUICKSTART.md](./QUICKSTART.md) - Setup environment
3. Read [frontend/BACKEND_API_INTEGRATION.md](./frontend/BACKEND_API_INTEGRATION.md) - API integration
4. Read [WORKFLOW.md](./WORKFLOW.md) - Git workflow
5. Start coding! Reference [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) as needed

### Backend Developer Path
1. Read [README.md](./README.md) - Understand project
2. Read [QUICKSTART.md](./QUICKSTART.md) - Setup environment
3. Read [backend/AI_SERVICE_INTEGRATION.md](./backend/AI_SERVICE_INTEGRATION.md) - AI service integration
4. Read [WORKFLOW.md](./WORKFLOW.md) - Git workflow
5. Start coding! Reference [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) as needed

### AI/ML Developer Path
1. Read [README.md](./README.md) - Understand project
2. Read [ai-service/README.md](./ai-service/README.md) - Hybrid AI architecture
3. Read [QUICKSTART.md](./QUICKSTART.md) - Test locally
4. Read [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) - Full system context
5. Start coding! Reference [WORKFLOW.md](./WORKFLOW.md) for integration flow

---

## 🎯 Common Tasks

### "I want to..."

**...understand the whole system**
→ Read [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)

**...start developing immediately**
→ Follow [QUICKSTART.md](./QUICKSTART.md)

**...integrate with another service**
- Frontend → Backend: [frontend/BACKEND_API_INTEGRATION.md](./frontend/BACKEND_API_INTEGRATION.md)
- Backend → AI: [backend/AI_SERVICE_INTEGRATION.md](./backend/AI_SERVICE_INTEGRATION.md)

**...configure the AI service**
→ Copy [ai-service/.env.example](./ai-service/.env.example) to `.env` and edit

**...understand the hybrid AI approach**
→ Read "Hybrid Approach Overview" in [ai-service/README.md](./ai-service/README.md)

**...see the full integration flow**
→ Check diagrams in [WORKFLOW.md](./WORKFLOW.md)

**...deploy to production**
→ See "Deployment Guide" in [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md)

**...contribute code**
→ Follow "Git Workflow" in [README.md](./README.md) or [WORKFLOW.md](./WORKFLOW.md)

---

## 🆘 Troubleshooting

### Service Won't Start
- **AI Service**: Check [ai-service/README.md](./ai-service/README.md) → "Configuration" section
- **Backend**: Check [backend/AI_SERVICE_INTEGRATION.md](./backend/AI_SERVICE_INTEGRATION.md) → "Environment Variables"
- **Frontend**: Check [frontend/BACKEND_API_INTEGRATION.md](./frontend/BACKEND_API_INTEGRATION.md) → "Environment Setup"

### Integration Issues
- **CORS errors**: Check [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) → "Troubleshooting" → "CORS"
- **Connection refused**: Check [QUICKSTART.md](./QUICKSTART.md) → "Troubleshooting"
- **API errors**: Check respective integration guides

### AI Service Specific
- **OCR not working**: [ai-service/README.md](./ai-service/README.md) → "OCR Prerequisites"
- **Gemini API errors**: [ai-service/README.md](./ai-service/README.md) → "Configuration" → "Gemini Settings"
- **Model training**: [ai-service/README.md](./ai-service/README.md) → "Hybrid Approach Overview"

---

## 📝 Document Maintenance

### When to Update Docs

**API Changes**
- Update [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) → "API Contracts"
- Update respective integration guides
- Notify all teams 24hrs before

**Configuration Changes**
- Update [ai-service/.env.example](./ai-service/.env.example)
- Update [ai-service/README.md](./ai-service/README.md) → "Configuration"

**New Features**
- Update [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) → "Service Responsibilities"
- Update [WORKFLOW.md](./WORKFLOW.md) if workflow changes

**Deployment Changes**
- Update [PROJECT_BLUEPRINT.md](./PROJECT_BLUEPRINT.md) → "Deployment Guide"

---

## 🔗 External Resources

### LLM Setup
- **Google Gemini API Key** (Free): https://aistudio.google.com/app/apikey
- **Ollama** (Local): https://ollama.com

### OCR Setup
- **Tesseract OCR** (Windows): https://github.com/UB-Mannheim/tesseract/wiki

### Deployment
- **Vercel** (Frontend): https://vercel.com
- **Render** (Backend/AI): https://render.com
- **Railway** (Alternative): https://railway.app

---

## 📊 Documentation Stats

| Document | Purpose | Audience | Length |
|----------|---------|----------|--------|
| README.md | Project overview | All | Short |
| QUICKSTART.md | Quick setup | All | Medium |
| PROJECT_BLUEPRINT.md | Complete guide | All | Long |
| WORKFLOW.md | Process & flows | All | Medium |
| ai-service/README.md | AI config | AI Team | Medium |
| backend/AI_SERVICE_INTEGRATION.md | Backend→AI | Backend | Long |
| frontend/BACKEND_API_INTEGRATION.md | Frontend→Backend | Frontend | Long |

**Total**: 7 main documents covering all aspects of development and deployment

---

## 💡 Tips

- **Bookmark this page** for quick navigation
- **Use Ctrl+F** to search within documents
- **Check diagrams** in WORKFLOW.md for visual understanding
- **Run QUICKSTART.md** before diving into code
- **Keep docs open** while developing for reference

---

*Last Updated: December 19, 2025*

**Questions?** Open an issue or ask in team chat!
