# AutoDev-AI - Autonomous Full-Stack Code Generation Platform

An open-source platform for generating production-ready full-stack applications using AI. Similar to Cursor, but for complete project generation.

## Features

- 🤖 AI-powered code generation using Ollama (deepseek-coder, CodeLlama, Mistral)
- 🏗️ Automatic full-stack scaffolding (Backend, Frontend, DevOps)
- 📦 Complete project structure with Docker setup
- 🔐 Local-only inference (no external APIs required)
- 🚀 Production-ready code generation
- 📊 Project status tracking and monitoring

## Tech Stack

### Backend
- **FastAPI** - High-performance async Python web framework
- **Python 3.11+** - Latest Python version
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - ORM with async support
- **Redis** - Job queue and caching
- **Ollama** - Local LLM inference engine

### Frontend
- **Next.js 14** - App Router with TypeScript
- **React 18** - Modern UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Prerequisites

- Docker and Docker Compose installed
- Ollama running locally (install from https://ollama.ai)
- At least 8GB RAM for AI model inference
- Git (for cloning)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd autodev-ai
```

### 2. Install and Run Ollama

```bash
# Download and install Ollama from https://ollama.ai
# After installation, pull required models:
ollama pull deepseek-coder
# Or use other models:
ollama pull codellama
ollama pull mistral
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Usage

### Generate a Project

1. Open http://localhost:3000 in your browser
2. Describe your project in the prompt field, e.g.:
   ```
   Build a task manager with authentication, PostgreSQL backend, 
   real-time updates using WebSockets, and a React dashboard with 
   task filtering and sorting.
   ```
3. Click "Generate Project"
4. Monitor progress on the status panel
5. Once complete, find your generated project in `generated_projects/{project-id}/`

### Example Prompts

- "Build a blog platform with user authentication, posts, comments, and search"
- "Create an e-commerce product catalog with filtering, sorting, and shopping cart"
- "Build a weather dashboard with 5-day forecast and location search"
- "Create a project management app with teams, tasks, and real-time collaboration"

## Project Structure

```
autodev-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py         # API endpoints
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py           # BaseAgent class
│   │   │   ├── requirement_agent.py
│   │   │   ├── architecture_agent.py
│   │   │   ├── backend_agent.py
│   │   │   ├── frontend_agent.py
│   │   │   └── devops_agent.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Configuration management
│   │   │   └── database.py       # Database setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── project.py        # SQLAlchemy models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── project.py        # Pydantic schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ollama_service.py # Ollama integration
│   │   │   ├── orchestrator.py   # Orchestration logic
│   │   │   └── project_builder.py # File generation
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── path_utils.py     # Path safety utilities
│   │       └── code_generator.py # Code generation helpers
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Home page
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   ├── PromptInput.tsx        # Project prompt input
│   │   └── ProjectStatus.tsx      # Status tracking UI
│   ├── services/
│   │   └── api.ts                # API client
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml            # Multi-container setup
├── README.md
└── generated_projects/           # Output directory for generated apps

```

## API Endpoints

### POST /api/generate
Generate a new project.

**Request:**
```json
{
  "prompt": "Build a task manager with authentication"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "task-manager",
  "prompt": "Build a task manager with authentication",
  "status": "queued",
  "created_at": "2024-02-24T12:00:00",
  "updated_at": "2024-02-24T12:00:00"
}
```

### GET /api/projects/{project_id}
Get project status.

**Response:**
```json
{
  "id": "uuid",
  "name": "task-manager",
  "status": "completed",
  "output_path": "/app/generated_projects/uuid",
  "created_at": "2024-02-24T12:00:00",
  "updated_at": "2024-02-24T12:00:15"
}
```

### GET /api/projects
List all projects.

## Environment Variables

Backend configuration in `.env`:

```env
# Database
DATABASE_URL=postgresql://autodev:autodev@postgres:5432/autodev

# Redis
REDIS_URL=redis://redis:6379/0

# Ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=deepseek-coder

# API
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development

# Projects
PROJECTS_BASE_PATH=/app/generated_projects
```

## Development

### Running Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Running Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

## Generated Project Structure

Each generated project includes:

```
generated_projects/{project-id}/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── __init__.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── .env.example
```

## Security Considerations

- ✅ Path traversal protection on file writes
- ✅ Filename sanitization
- ✅ Generated code isolated in `generated_projects/`
- ✅ No automatic code execution
- ✅ Local-only inference (no data sent to external servers)
- ✅ Database credentials managed via environment variables

## AI Agents

The system uses specialized agents for different aspects of code generation:

1. **RequirementAgent** - Analyzes user prompts and extracts requirements
2. **ArchitectureAgent** - Plans application architecture
3. **BackendAgent** - Generates FastAPI backend code
4. **FrontendAgent** - Generates Next.js frontend code
5. **DevOpsAgent** - Generates Docker configuration

Each agent:
- Accepts structured input
- Returns structured JSON output
- Uses Ollama for inference
- Supports temperature control for creativity/consistency

## Troubleshooting

### Ollama Connection Issues

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check model is downloaded
ollama list

# Pull model if needed
ollama pull deepseek-coder
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker logs autodev-postgres

# Reset database
docker-compose down -v
docker-compose up
```

### Frontend API Connection

Update `NEXT_PUBLIC_API_URL` environment variable in `docker-compose.yml`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check existing GitHub issues
2. Review the troubleshooting section
3. Check logs with `docker-compose logs -f`

## Roadmap

- [ ] Multi-language support (Go, Node.js, Rust)
- [ ] Advanced testing framework generation
- [ ] CI/CD pipeline generation
- [ ] GraphQL support
- [ ] Microservices architecture support
- [ ] Mobile app generation
- [ ] Advanced caching strategies
- [ ] Custom model fine-tuning support

## Acknowledgments

- Built with FastAPI, Next.js, and Ollama
- Inspired by Cursor and similar AI-powered tools
- Community-driven development

---

**AutoDev-AI** - Building the future of code generation, one project at a time.
