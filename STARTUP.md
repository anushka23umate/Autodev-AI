# AutoDev-AI - Complete Setup & Startup Guide

## Prerequisites Check

Before starting, ensure you have:
- Docker & Docker Compose installed
- Ollama installed and running
- At least 8GB RAM available
- 10GB free disk space

## Step 1: Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, install Ollama from https://ollama.ai
# Start Ollama:
ollama serve
```

## Step 2: Pull Required AI Models

Run this in a NEW terminal (keep Ollama serving in the first):

```bash
# Pull deepseek-coder (recommended for code generation)
ollama pull deepseek-coder

# Alternative models:
ollama pull codellama
ollama pull mistral

# Verify model is loaded
ollama list
```

## Step 3: Clone & Setup Project

```bash
# Navigate to your workspace
cd d:\FULL\autodev-ai

# Verify structure
dir
# Should show: backend/, frontend/, docker-compose.yml, README.md, setup.sh
```

## Step 4: Start Services

### Windows PowerShell

```bash
# Start services (builds Docker images)
docker-compose up --build

# First run will take 3-5 minutes to build images
# Wait until you see:
# - "backend: INFO:     Uvicorn running on http://0.0.0.0:8000"
# - "frontend: compiled client and server successfully"
```

### Linux/Mac

```bash
docker-compose up --build
```

## Step 5: Verify Services are Running

Open a new terminal and run:

```bash
# Check all containers are running
docker-compose ps

# Should show 4 containers: postgres, redis, backend, frontend
# All with status "Up"
```

## Step 6: Access the Application

### Frontend Dashboard
- URL: http://localhost:3000
- You should see the AutoDev-AI interface with prompt input

### Backend API
- URL: http://localhost:8000
- Health check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

### Database
- PostgreSQL: localhost:5432
- User: autodev
- Password: autodev
- Database: autodev

### Redis
- Redis: localhost:6379

## Step 7: Generate Your First Project

1. Open http://localhost:3000
2. Copy and paste this prompt:
   ```
   Build a simple task manager with FastAPI backend, 
   Next.js frontend, PostgreSQL database, user authentication, 
   and task CRUD operations.
   ```
3. Click "Generate Project"
4. Watch the status panel update through the pipeline:
   - Queued → Analyzing → Generating Backend → Generating Frontend → Dockerizing → Completed
5. Once complete, find your generated project in `generated_projects/` folder

## Troubleshooting

### Container Won't Start

```bash
# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart containers
docker-compose restart
```

### Ollama Connection Error

```bash
# Verify Ollama is running on port 11434
curl http://localhost:11434/api/tags

# If error, ensure:
# 1. Ollama is installed
# 2. Ollama process is running (ollama serve)
# 3. Not behind firewall blocking localhost:11434
```

### Database Connection Error

```bash
# Reset database
docker-compose down -v  # Removes all volumes
docker-compose up --build
```

### Memory Issues

If you get OOM errors:
```bash
# Increase Docker memory in Docker Desktop settings
# Minimum recommended: 4GB allocated to Docker
```

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Rebuild specific service
docker-compose up --build backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats

# Remove all AutoDev-AI containers and images
docker-compose down -v
docker rmi autodev-ai-backend autodev-ai-frontend
```

## File Locations

- **Generated Projects**: `generated_projects/` directory
- **Backend Code**: `backend/` directory
- **Frontend Code**: `frontend/` directory
- **Database Data**: Docker volume (persists between restarts)
- **Configuration**: `backend/.env` and `.env` in generated projects

## Next Steps

1. Try generating different types of projects:
   - Blog platform with comments
   - E-commerce product catalog
   - Weather dashboard
   - Real-time chat application

2. Explore the generated code in `generated_projects/`

3. Run generated projects locally:
   ```bash
   cd generated_projects/{project-id}
   docker-compose up --build
   ```

4. Check API documentation at http://localhost:8000/docs

## Production Deployment

For production use:

1. Update environment variables in `docker-compose.yml`
2. Use stronger database credentials
3. Enable HTTPS/SSL
4. Set up proper logging and monitoring
5. Use managed database service (AWS RDS, Google Cloud SQL)
6. Deploy to Kubernetes or managed container service

## Support & Issues

- Check logs: `docker-compose logs`
- Verify prerequisites are installed correctly
- Ensure ports 3000, 8000, 5432, 6379, 11434 are available
- Check GitHub issues if problems persist

## Important Notes

⚠️ **Keep Ollama Running**: Ollama must be running (ollama serve) for the system to work
⚠️ **First Generation Takes Time**: First API call may take 30-60 seconds as models load
⚠️ **Local Only**: All processing is local - no cloud services used
⚠️ **Disk Space**: Generated projects consume disk space - monitor `/generated_projects`

## Common Prompts to Try

```
# E-commerce
"Build an e-commerce store with product catalog, shopping cart, 
and checkout system using FastAPI and PostgreSQL"

# Social Media
"Create a simple social media platform with posts, likes, 
comments, and user profiles"

# Project Management
"Build a project management tool with teams, projects, tasks, 
and progress tracking"

# Real-time Chat
"Build a real-time chat application with rooms, user presence, 
and message history"

# Analytics Dashboard
"Create an analytics dashboard with charts, user activity tracking, 
and export features"
```

---

**Happy coding! 🚀**
