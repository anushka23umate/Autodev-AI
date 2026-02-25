# AutoDev-AI Architecture & Implementation Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
│              (http://localhost:3000)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   NEXT.JS FRONTEND                          │
│  - React 18 (App Router)                                    │
│  - Tailwind CSS                                             │
│  - Axios API Client                                         │
│  - Project Status Dashboard                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ JSON/HTTP
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND                            │
│  - API Routes & Controllers                                 │
│  - Project Orchestration                                    │
│  - Agent Coordination                                       │
│  - File Generation & Management                             │
└───┬────────────┬────────────┬──────────────┬────────────────┘
    │            │            │              │
    ▼            ▼            ▼              ▼
┌────────┐  ┌────────┐  ┌──────────┐  ┌────────────┐
│ Agents │  │Database│  │  Ollama  │  │   Redis    │
│        │  │        │  │          │  │            │
│ - Req  │  │Postgres│  │ deepseek │  │ Job Queue  │
│ - Arch │  │15      │  │ codellama│  │ Caching    │
│ - Back │  │        │  │ mistral  │  │            │
│ - Front│  │        │  │          │  │            │
│ - DevOps│ │        │  │(local)   │  │            │
└────────┘  └────────┘  └──────────┘  └────────────┘
```

## Core Components

### 1. Frontend Layer (Next.js)

**Location**: `frontend/`

**Key Files**:
- `app/page.tsx` - Main dashboard with prompt input
- `components/PromptInput.tsx` - User input form
- `components/ProjectStatus.tsx` - Real-time status tracking
- `services/api.ts` - Backend API client

**Features**:
- Real-time project status updates (polls every 2 seconds)
- Interactive prompt input with examples
- Progress visualization with step indicators
- Error handling and user feedback

### 2. Backend API (FastAPI)

**Location**: `backend/app/`

**Key Files**:
- `main.py` - Application initialization and middleware setup
- `api/routes.py` - HTTP endpoints

**Endpoints**:
```
POST   /api/generate          - Create new project
GET    /api/projects/{id}     - Get project status
GET    /api/projects          - List all projects
GET    /health                - Health check
GET    /docs                  - API documentation
```

### 3. AI Agent System

**Location**: `backend/app/agents/`

**Architecture**:
```
BaseAgent (Abstract)
├── RequirementAgent
│   └── Analyzes user prompts → Requirements JSON
├── ArchitectureAgent
│   └── Plans system architecture → Architecture JSON
├── BackendAgent
│   └── Generates FastAPI code
├── FrontendAgent
│   └── Generates Next.js code
└── DevOpsAgent
    └── Generates Docker config
```

**Agent Flow**:
```
Prompt
  │
  ▼
RequirementAgent (Extract: features, stack, complexity)
  │
  ▼
ArchitectureAgent (Plan: APIs, database, pages)
  │
  ├─────────────────┬──────────────────┬─────────────────┐
  ▼                 ▼                  ▼                 ▼
BackendAgent   FrontendAgent    DevOpsAgent         ProjectBuilder
  │                 │                  │                 │
  ▼                 ▼                  ▼                 ▼
Backend Code   Frontend Code     Docker Config    File Generation
  │                 │                  │                 │
  └─────────────────┴──────────────────┴─────────────────┘
                     │
                     ▼
            generated_projects/{id}/
```

### 4. Project Builder

**Location**: `backend/app/services/project_builder.py`

**Responsibilities**:
- Creates directory structure
- Writes generated code files
- Generates configuration files
- Ensures path traversal protection

**Safety Features**:
```python
# Path validation
get_project_path(project_id)  # Validates within base_path

# Filename sanitization
sanitize_filename(name)  # Removes unsafe characters

# Safe file writing
write_file_safely(path, content)  # Checks base_path restriction
```

### 5. Ollama Integration

**Location**: `backend/app/services/ollama_service.py`

**Capabilities**:
- HTTP API calls to local Ollama
- JSON response generation
- Temperature/creativity control
- Model selection (deepseek-coder, codellama, mistral)

**Flow**:
```python
ollama_service.generate(
    prompt="Generate Python code...",
    temperature=0.7,        # Creativity
    system_prompt="..."     # Instructions
)
```

### 6. Database Schema

**Location**: `backend/app/models/project.py`

**Project Table**:
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    prompt TEXT,
    status ENUM(queued, analyzing, ..., completed, failed),
    output_path VARCHAR(512),
    error_message TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Status Lifecycle**:
```
queued → analyzing → generating_backend 
       → generating_frontend → dockerizing 
       → completed (or failed)
```

## Deployment Flow

```
1. User submits prompt
   ▼
2. FastAPI creates Project record (status: queued)
   ▼
3. Background task spawns orchestrator
   ▼
4. RequirementAgent analyzes prompt
   ▼
5. ArchitectureAgent plans system
   ▼
6. BackendAgent generates code (in parallel with Frontend)
   ▼
7. FrontendAgent generates code
   ▼
8. DevOpsAgent generates Docker config
   ▼
9. ProjectBuilder writes all files to disk
   ▼
10. Status updated to completed
   ▼
11. Frontend polls and displays completion
```

## File Structure Generated

Each project generates:

```
generated_projects/{project_id}/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # SQLAlchemy models
│   │   └── routes.py        # API endpoints
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Backend containerization
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   └── globals.css      # Styling
│   ├── components/          # React components
│   ├── services/
│   │   └── api.ts           # API client
│   ├── package.json         # npm dependencies
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml       # Multi-container setup
├── .env.example             # Environment template
└── README.md                # Project documentation
```

## Data Flow for Prompt Processing

```
POST /api/generate
  │
  ├─ Validate prompt (10-2000 chars)
  │
  ├─ Create Project record
  │   └─ status: "queued"
  │
  ├─ Background task: _run_orchestration()
  │   │
  │   ├─ Update status: "analyzing"
  │   ├─ Call RequirementAgent
  │   │   └─ Ollama: "Analyze this requirement..."
  │   │   └─ Returns: {project_name, features, tech_stack, ...}
  │   │
  │   ├─ Update status: "generating_backend"
  │   ├─ Call BackendAgent
  │   │   └─ Ollama: "Generate FastAPI code..."
  │   │   └─ Returns: {main_py, models_py, routes_py}
  │   │
  │   ├─ Update status: "generating_frontend"
  │   ├─ Call FrontendAgent
  │   │   └─ Ollama: "Generate Next.js code..."
  │   │   └─ Returns: {layout_tsx, page_tsx, api_service}
  │   │
  │   ├─ Update status: "dockerizing"
  │   ├─ Call DevOpsAgent
  │   │   └─ Ollama: "Generate Docker config..."
  │   │   └─ Returns: {dockerfile, docker-compose}
  │   │
  │   ├─ Call ProjectBuilder
  │   │   └─ Write files to generated_projects/{id}/
  │   │
  │   └─ Update status: "completed"
  │
  └─ Return Project response
      {
        "id": "uuid",
        "status": "queued",
        "created_at": "..."
      }
```

## Security Implementation

### Path Traversal Protection
```python
def get_project_path(project_id: str) -> Path:
    base_path = Path(settings.PROJECTS_BASE_PATH)
    project_path = base_path / str(project_id)
    
    # Validate path is within base_path
    try:
        project_path.resolve().relative_to(base_path.resolve())
    except ValueError:
        raise ValueError("Path traversal detected")
```

### Filename Sanitization
```python
def sanitize_filename(filename: str) -> str:
    # Remove unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limit length
    return filename[:255]
```

### Isolated Code Generation
- All generated files within `generated_projects/`
- No execution of generated code
- No external API calls (local Ollama only)
- Environment variables protected

## Scaling Considerations

### Horizontal Scaling
- Stateless backend (can run multiple instances)
- Database for state persistence
- Redis for job queue (if needed)

### Performance Optimization
- Async/await for all I/O
- Connection pooling (SQLAlchemy)
- Model caching in Ollama
- Parallel agent execution possible

### Monitoring & Logging
- Structured logging with project IDs
- Database tracking of all projects
- Error messages preserved for debugging
- Status polling for long operations

## Technology Choices

| Component | Choice | Why |
|-----------|--------|-----|
| Backend | FastAPI | Async, performance, auto-docs |
| Frontend | Next.js | React, server-side, deployment |
| Database | PostgreSQL | Reliability, ACID, complex queries |
| Cache | Redis | Performance, job queue |
| LLM | Ollama | Local, open-source, no API calls |
| UI | Tailwind | Utility-first, rapid development |
| Containerization | Docker | Consistency, deployment |

## Environment Variables

```env
# Database connection
DATABASE_URL=postgresql://user:pass@host:5432/db

# Ollama configuration
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=deepseek-coder

# Project management
PROJECTS_BASE_PATH=/app/generated_projects

# Redis (for future job queue)
REDIS_URL=redis://redis:6379/0

# API configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

## Extension Points

### Adding New Agents
```python
class YourNewAgent(BaseAgent):
    def __init__(self):
        super().__init__("YourAgentName")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your logic here
        result = await self.call_ollama(prompt)
        return result
```

### Adding New Endpoints
```python
@router.post("/api/your-endpoint")
async def your_endpoint(request: YourRequest, db: AsyncSession = Depends(get_db)):
    # Your logic here
    return {"result": "..."}
```

### Custom Code Generators
Extend `ProjectBuilder` to generate additional file types or configurations.

---

**Last Updated**: February 2024
**Architecture Version**: 1.0.0
