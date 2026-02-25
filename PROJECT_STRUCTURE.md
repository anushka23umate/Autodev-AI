# AutoDev-AI - Complete Project Structure

## File Tree

```
autodev-ai/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Package initialization
│   │   ├── main.py                  # FastAPI application entry point
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py            # API endpoints (/generate, /projects)
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # BaseAgent abstract class
│   │   │   ├── requirement_agent.py # Extracts requirements from prompt
│   │   │   ├── architecture_agent.py# Plans system architecture
│   │   │   ├── backend_agent.py     # Generates FastAPI code
│   │   │   ├── frontend_agent.py    # Generates Next.js code
│   │   │   └── devops_agent.py      # Generates Docker configuration
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Settings & configuration
│   │   │   └── database.py          # SQLAlchemy setup & connection
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── project.py           # SQLAlchemy Project model
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── project.py           # Pydantic request/response schemas
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ollama_service.py    # Ollama LLM integration
│   │   │   ├── orchestrator.py      # Agent coordination pipeline
│   │   │   └── project_builder.py   # File generation & project structure
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── path_utils.py        # Path safety & validation
│   │       └── code_generator.py    # Code formatting utilities
│   │
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend containerization
│   ├── .env.example                 # Environment template
│   └── .gitignore                   # Git ignore rules
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx               # Root layout component
│   │   ├── page.tsx                 # Home page with prompt input
│   │   ├── globals.css              # Global styling
│   │   └── .gitkeep
│   │
│   ├── components/
│   │   ├── PromptInput.tsx          # Prompt input form component
│   │   ├── ProjectStatus.tsx        # Project status display component
│   │   └── .gitkeep
│   │
│   ├── services/
│   │   ├── api.ts                   # Axios API client
│   │   └── .gitkeep
│   │
│   ├── package.json                 # npm dependencies
│   ├── next.config.js               # Next.js configuration
│   ├── postcss.config.js            # PostCSS & Tailwind config
│   ├── tailwind.config.ts           # Tailwind CSS configuration
│   ├── tsconfig.json                # TypeScript configuration
│   ├── Dockerfile                   # Frontend containerization
│   ├── .gitignore                   # Git ignore rules
│   └── .gitkeep
│
├── generated_projects/              # Output directory for generated apps
│   └── .gitkeep
│
├── docker-compose.yml               # Multi-container orchestration
├── README.md                         # Main documentation
├── STARTUP.md                        # Setup & startup guide
├── ARCHITECTURE.md                  # Architecture & implementation details
├── PROJECT_STRUCTURE.md             # This file - file listing
├── setup.sh                          # Linux/Mac setup script
├── setup.bat                         # Windows setup script
├── .gitignore                        # Root .gitignore
└── LICENSE                           # MIT License (if included)
```

## File Descriptions

### Backend Core

| File | Purpose | Key Features |
|------|---------|--------------|
| `app/main.py` | FastAPI initialization | Middleware, lifespan, routes |
| `app/api/routes.py` | HTTP endpoints | POST /generate, GET /projects |
| `app/core/config.py` | Configuration | Settings from environment |
| `app/core/database.py` | Database setup | AsyncSession, ORM initialization |

### Agents

| File | Purpose | Output |
|------|---------|--------|
| `agents/base.py` | Agent base class | Ollama integration methods |
| `agents/requirement_agent.py` | Requirement parsing | Project name, features, tech stack |
| `agents/architecture_agent.py` | System architecture | API endpoints, database schema |
| `agents/backend_agent.py` | Backend generation | main.py, models.py, routes.py |
| `agents/frontend_agent.py` | Frontend generation | layout.tsx, page.tsx, components |
| `agents/devops_agent.py` | DevOps generation | Dockerfile, docker-compose, README |

### Services

| File | Purpose | Key Classes |
|------|---------|-------------|
| `services/ollama_service.py` | LLM integration | OllamaService |
| `services/orchestrator.py` | Pipeline coordination | ProjectOrchestrator |
| `services/project_builder.py` | File generation | ProjectBuilder |

### Data Layer

| File | Purpose | Entities |
|------|---------|----------|
| `models/project.py` | Database models | Project (SQLAlchemy) |
| `schemas/project.py` | API schemas | ProjectCreate, ProjectResponse |

### Frontend Components

| File | Purpose | Features |
|------|---------|----------|
| `app/layout.tsx` | Root layout | Navigation, metadata, providers |
| `app/page.tsx` | Home page | Prompt input, project list, status |
| `components/PromptInput.tsx` | Input form | Text input, example prompts |
| `components/ProjectStatus.tsx` | Status display | Progress tracker, status updates |
| `services/api.ts` | API client | Axios instance, interceptors |

### Configuration Files

| File | Purpose | Content |
|------|---------|---------|
| `docker-compose.yml` | Container orchestration | Services: postgres, redis, backend, frontend |
| `Dockerfile` (backend) | Backend containerization | Python 3.11 slim, dependencies |
| `Dockerfile` (frontend) | Frontend containerization | Node.js alpine, multi-stage build |
| `package.json` | npm dependencies | React, Next.js, Axios, Tailwind |
| `next.config.js` | Next.js settings | App Router, optimization |
| `tailwind.config.ts` | Tailwind theme | Color scheme, extensions |
| `tsconfig.json` | TypeScript settings | Strict mode, paths, compilation |

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Main documentation | All users |
| `STARTUP.md` | Setup instructions | New users |
| `ARCHITECTURE.md` | Technical details | Developers |
| `PROJECT_STRUCTURE.md` | This file | Reference |

### Setup Scripts

| File | Purpose | Platform |
|------|---------|----------|
| `setup.sh` | Automated setup | Linux/Mac |
| `setup.bat` | Automated setup | Windows |

## Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    prompt TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'queued',
    output_path VARCHAR(512),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Status Enum Values
- `queued` - Waiting to be processed
- `analyzing` - Extracting requirements
- `generating_backend` - Creating backend code
- `generating_frontend` - Creating frontend code
- `dockerizing` - Generating Docker config
- `completed` - Successfully generated
- `failed` - Generation failed

## Environment Variables Required

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Ollama LLM
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=deepseek-coder

# Redis
REDIS_URL=redis://redis:6379/0

# Paths
PROJECTS_BASE_PATH=/app/generated_projects

# API
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development
```

## Key Dependencies

### Backend (Python)
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.0
- httpx==0.25.2
- psycopg2-binary==2.9.9
- redis==5.0.1

### Frontend (Node.js)
- react==18.2.0
- next==14.0.3
- tailwindcss==3.3.6
- axios==1.6.2
- typescript==5.3.3

### External Services
- PostgreSQL 15
- Redis 7
- Ollama (local)

## Generated Project Structure

Each generated project follows this structure:

```
generated_projects/{project_id}/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   ├── services/
│   │   └── api.ts
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## File Sizes Reference

| Component | Est. Size | Notes |
|-----------|-----------|-------|
| Backend codebase | ~50 KB | Python source |
| Frontend codebase | ~30 KB | TypeScript/React |
| Docker images | ~800 MB | Python 3.11, Node.js |
| Database (empty) | ~5 MB | PostgreSQL |
| Generated project | ~10 KB | Per project |

## Development Workflow

1. **Code Changes**
   - Edit files in `backend/app/` or `frontend/`
   - Use hot reload (uvicorn reload, next dev)

2. **Testing**
   - Backend: `pytest backend/`
   - Frontend: `npm test`

3. **Building**
   - `docker-compose build`
   - `docker-compose up`

4. **Deployment**
   - Push to registry
   - Deploy docker-compose.yml

## Common File Edits

### Adding a New API Endpoint
Edit `backend/app/api/routes.py`

### Adding a New Frontend Page
1. Create file in `frontend/app/`
2. Update routing (Next.js App Router)
3. Add API calls in services

### Adding Python Dependency
Edit `backend/requirements.txt` then rebuild

### Adding npm Dependency
Edit `frontend/package.json` then rebuild

### Configuring AI Models
Edit `backend/app/core/config.py` OLLAMA_MODEL

## Testing Checklist

- [ ] Docker containers start (`docker-compose up`)
- [ ] Frontend accessible (http://localhost:3000)
- [ ] Backend API accessible (http://localhost:8000)
- [ ] API documentation loads (/docs)
- [ ] Ollama connection works
- [ ] Database initializes
- [ ] Generate project succeeds
- [ ] Files created in generated_projects/

---

**Last Updated**: February 2024
**Total Files**: 40+
**Total Lines of Code**: 3000+
