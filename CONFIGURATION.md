# AutoDev-AI Configuration Summary

## System Composition

### Services
```
Frontend (Next.js)        → Port 3000
Backend (FastAPI)         → Port 8000
PostgreSQL Database       → Port 5432
Redis Cache               → Port 6379
Ollama LLM (external)     → Port 11434
```

### Technologies
```
Backend:      FastAPI + SQLAlchemy + Pydantic + Python 3.11
Frontend:     Next.js + React 18 + TypeScript + Tailwind CSS
Database:     PostgreSQL 15
Cache:        Redis 7
LLM:          Ollama (deepseek-coder, codellama, mistral)
Containers:   Docker + Docker Compose
```

---

## Default Credentials

### Database
```
Host:     postgres (or localhost:5432)
User:     autodev
Password: autodev
Database: autodev
```

### Environment
```
API_HOST:                0.0.0.0
API_PORT:                8000
ENVIRONMENT:             development
PROJECTS_BASE_PATH:      /app/generated_projects
```

### Ollama
```
Base URL:    http://ollama:11434 (Docker)
             http://localhost:11434 (Local)
Default:     deepseek-coder
```

---

## Configuration Files

### Backend Configuration
**File**: `backend/app/core/config.py`

```python
class Settings:
    DATABASE_URL = "postgresql://autodev:autodev@postgres:5432/autodev"
    OLLAMA_BASE_URL = "http://ollama:11434"
    OLLAMA_MODEL = "deepseek-coder"
    REDIS_URL = "redis://redis:6379/0"
    PROJECTS_BASE_PATH = "/app/generated_projects"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    ENVIRONMENT = "development"
```

### Environment Variables
**File**: `backend/.env.example`

```env
DATABASE_URL=postgresql://autodev:autodev@postgres:5432/autodev
REDIS_URL=redis://redis:6379/0
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=deepseek-coder
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
PROJECTS_BASE_PATH=/app/generated_projects
```

### Docker Compose
**File**: `docker-compose.yml`

Services:
- `postgres`: PostgreSQL 15-alpine
- `redis`: Redis 7-alpine
- `backend`: FastAPI application
- `frontend`: Next.js application

---

## Ports Reference

| Service | Port | Internal | External | Purpose |
|---------|------|----------|----------|---------|
| Frontend | 3000 | - | :3000 | Web UI |
| Backend | 8000 | - | :8000 | API |
| PostgreSQL | 5432 | postgres:5432 | :5432 | Database |
| Redis | 6379 | redis:6379 | :6379 | Cache |
| Ollama | 11434 | N/A | :11434 | LLM (external) |

---

## API Configuration

### Backend Entry Point
**File**: `backend/app/main.py`

```python
app = FastAPI(
    title="AutoDev-AI",
    version="1.0.0",
    lifespan=lifespan
)
```

### Routes Prefix
All API endpoints: `/api/*`

### Health Check
```
GET http://localhost:8000/health
Response: {"status": "healthy"}
```

### API Documentation
```
http://localhost:8000/docs       (Swagger UI)
http://localhost:8000/redoc      (ReDoc)
http://localhost:openapi.json    (OpenAPI spec)
```

---

## Database Configuration

### Connection Pool
```python
engine = create_async_engine(
    database_url,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
```

### Tables
- `projects` - Application projects

### Initialization
Automatic on application startup via `init_db()`

---

## Ollama Configuration

### Connection
```
OLLAMA_BASE_URL = "http://ollama:11434"
TIMEOUT = 300 seconds (5 minutes)
```

### Models Supported
- `deepseek-coder` (recommended)
- `codellama`
- `mistral`

### Parameters
- `temperature`: 0.3 (for JSON), 0.5-0.7 (for code)
- `top_p`: 0.9
- `stream`: False (full response)

---

## Frontend Configuration

### Next.js Settings
**File**: `frontend/next.config.js`

```javascript
{
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true
  }
}
```

### API URL
```
Local:       http://localhost:8000/api
Production:  Set via NEXT_PUBLIC_API_URL
```

### Build Output
```
.next/          - Build artifacts
node_modules/   - Dependencies
public/         - Static files
```

---

## Tailwind CSS Configuration

**File**: `frontend/tailwind.config.ts`

- Content paths: `./app/**/*.{js,ts,jsx,tsx,mdx}`
- Extensions: `./components/**/*.{js,ts,jsx,tsx,mdx}`
- Plugins: None

---

## TypeScript Configuration

**File**: `frontend/tsconfig.json`

- Target: ES2020
- Module: ESNext
- Strict: true
- JSX: preserve (Next.js)

---

## Docker Configuration

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
COPY --from=builder /app/.next ...
```

---

## Network Configuration

### Docker Network
- Name: `autodev-network`
- Type: Bridge
- Hosts can access via service names:
  - `postgres` → PostgreSQL
  - `redis` → Redis
  - `backend` → FastAPI
  - `frontend` → Next.js

---

## Volume Configuration

### Persistent Volumes
```yaml
postgres_data:      # PostgreSQL data persistence
generated_projects: # Generated project output
```

### Bind Mounts (Development)
```yaml
./backend:/app           # Backend code (hot reload)
./frontend:/app          # Frontend code (hot reload)
```

---

## Security Configuration

### CORS
**File**: `backend/app/main.py`

```python
allow_origins=["*"]           # Configure for production
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### Input Validation
- Pydantic models enforce types
- Field length limits
- Special character sanitization

### Path Protection
- All file writes within `generated_projects/`
- Path traversal validation
- Filename sanitization

---

## Performance Configuration

### Database
- Connection pool: 20 connections
- Max overflow: 0
- Pre-ping: Enabled (health check)

### Async
- All I/O operations async
- Uvicorn workers: 1 (configure for production)
- FastAPI automatic request handling

### Frontend
- Code splitting enabled
- Image optimization available
- CSS minification

---

## Logging Configuration

### Backend
**File**: `backend/app/main.py`

```python
logging.basicConfig(level=logging.INFO)
```

### Levels
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

---

## Error Handling

### Backend
- Try/except blocks in routes
- HTTPException for HTTP errors
- Logging of all errors

### Frontend
- Error boundaries (future)
- API error handling
- User-friendly messages

---

## Session Management

### Database Sessions
- Async session factory
- Automatic cleanup
- Connection pooling

### State Management
- Database-backed state
- Status tracking
- Error persistence

---

## File Paths

### Project Base
```
/app/generated_projects/        # Inside container
./generated_projects/           # Local mount
```

### Backend
```
/app/                           # Container working directory
./backend/                      # Local directory
```

### Frontend
```
/app/                           # Container working directory
./frontend/                     # Local directory
```

---

## Customization

### Change Model
Edit `backend/app/core/config.py`:
```python
OLLAMA_MODEL = "codellama"  # Change default
```

### Change Database
Edit `backend/app/core/config.py`:
```python
DATABASE_URL = "postgresql://new_user:new_pass@host:5432/db"
```

### Change API Port
Edit `docker-compose.yml`:
```yaml
ports:
  - "9000:8000"  # Change host port
```

### Change Frontend URL
Edit `docker-compose.yml`:
```yaml
environment:
  NEXT_PUBLIC_API_URL: http://api.example.com
```

---

## Monitoring Points

### Backend Health
```bash
curl http://localhost:8000/health
```

### Database Status
```bash
docker-compose exec postgres psql -U autodev -d autodev -c "SELECT version();"
```

### Service Status
```bash
docker-compose ps
```

### Resource Usage
```bash
docker stats
```

---

## Production Checklist

- [ ] Change default credentials
- [ ] Update CORS allowed origins
- [ ] Configure HTTPS/SSL
- [ ] Set ENVIRONMENT=production
- [ ] Setup database backups
- [ ] Configure monitoring
- [ ] Setup error tracking
- [ ] Enable rate limiting
- [ ] Setup logging aggregation
- [ ] Configure CDN (frontend)
- [ ] Setup autoscaling
- [ ] Configure health checks

---

## Troubleshooting Configuration

### Port Conflict
```bash
# Find process using port
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "9000:8000"
```

### Database Connection
```bash
# Test connection
docker-compose exec backend python -c "
from app.core.database import engine
print(engine.url)
"
```

### Ollama Connection
```bash
# Test Ollama
curl http://localhost:11434/api/tags
```

---

## Version Information

| Component | Version |
|-----------|---------|
| Python | 3.11+ |
| FastAPI | 0.104.1 |
| SQLAlchemy | 2.0.23 |
| Node.js | 18+ |
| Next.js | 14.0.3 |
| React | 18.2.0 |
| PostgreSQL | 15 |
| Redis | 7 |
| Docker | Latest |

---

## Configuration as Code

All configuration is codified:
- ✅ Environment variables (`.env`)
- ✅ Docker Compose (YAML)
- ✅ Python settings (`config.py`)
- ✅ Next.js config (`next.config.js`)
- ✅ Tailwind config (`tailwind.config.ts`)
- ✅ TypeScript config (`tsconfig.json`)

No UI configuration needed - everything is declarative.

---

**Configuration Document**: 1.0.0
**Last Updated**: February 2024
**Status**: ✅ Complete
