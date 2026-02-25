# AutoDev-AI - Quick Reference & Commands

## Quick Start (30 seconds)

```bash
# 1. Ensure Ollama is running
ollama serve  # in one terminal

# 2. Start the system
cd autodev-ai
docker-compose up --build

# 3. Open browser
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

## Common Commands

### Docker Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f                 # All services
docker-compose logs -f backend         # Backend only
docker-compose logs -f frontend        # Frontend only

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Remove everything
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats
```

### Development

```bash
# Backend local development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend local development
cd frontend
npm install
npm run dev

# Type checking
cd frontend
npm run build
```

### Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U autodev -d autodev

# View projects table
SELECT * FROM projects;

# Delete all projects
DELETE FROM projects;

# Reset database
docker-compose down -v && docker-compose up
```

### Debugging

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# API health check
curl http://localhost:8000/health

# List running containers
docker ps

# Check container status
docker-compose ps

# View container IP
docker inspect <container_id>
```

## API Endpoints

### Generate Project
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Build a task manager with authentication"
  }'
```

### Get Project Status
```bash
curl http://localhost:8000/api/projects/{project-id}
```

### List All Projects
```bash
curl "http://localhost:8000/api/projects?limit=50&offset=0"
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | postgresql://autodev:autodev@postgres:5432/autodev | Database connection |
| `OLLAMA_BASE_URL` | http://ollama:11434 | LLM inference |
| `OLLAMA_MODEL` | deepseek-coder | Default AI model |
| `REDIS_URL` | redis://redis:6379/0 | Caching/queue |
| `PROJECTS_BASE_PATH` | /app/generated_projects | Output directory |
| `API_PORT` | 8000 | Backend port |
| `ENVIRONMENT` | development | Environment type |

## Useful URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User interface |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
| Health | http://localhost:8000/health | Status check |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Cache |
| Ollama | localhost:11434 | LLM service |

## Prompt Examples

### E-commerce
```
Build a complete e-commerce platform with product catalog, 
shopping cart, user authentication, payment processing, 
and order management using PostgreSQL and FastAPI.
```

### Social Media
```
Create a social media application with user profiles, 
posts, likes, comments, followers system, and real-time 
notifications using Next.js and FastAPI.
```

### Project Management
```
Build a project management tool with teams, projects, 
tasks, subtasks, progress tracking, and team collaboration 
features using PostgreSQL and FastAPI.
```

### Analytics Dashboard
```
Create an analytics dashboard that displays user activity, 
metrics, charts, and reports with export functionality 
using React and FastAPI.
```

### Real-time Chat
```
Build a real-time chat application with private messages, 
group chats, user presence, typing indicators, and message 
history using WebSockets.
```

## Troubleshooting

### Issue: "Ollama connection refused"
```bash
# Solution: Start Ollama
ollama serve

# Verify:
curl http://localhost:11434/api/tags
```

### Issue: "Port already in use"
```bash
# Find process using port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

### Issue: "Database connection failed"
```bash
# Solution: Reset database
docker-compose down -v
docker-compose up

# Check database status
docker-compose logs postgres
```

### Issue: "Out of memory"
```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory: 4GB+
```

### Issue: "Build fails"
```bash
# Clean rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

## File Locations

| Item | Location |
|------|----------|
| Generated projects | `./generated_projects/` |
| Backend code | `./backend/app/` |
| Frontend code | `./frontend/` |
| Database config | `./backend/.env` |
| Environment template | `./backend/.env.example` |
| Docker config | `./docker-compose.yml` |
| Documentation | `./README.md`, `./ARCHITECTURE.md` |

## Performance Tips

1. **Model Selection**
   - `deepseek-coder` - Best for code, requires more resources
   - `codellama` - Balanced, good for all tasks
   - `mistral` - Fastest, less detailed

2. **Optimization**
   ```bash
   # Increase model cache
   export OLLAMA_NUM_GPU=1  # Use GPU if available
   
   # Adjust temperature (lower = more accurate)
   # 0.1 = deterministic, 0.7 = creative
   ```

3. **Resource Management**
   - Monitor Docker stats: `docker stats`
   - Limit running containers
   - Delete old generated projects

## Security Checklist

- [ ] Ollama access restricted to localhost only
- [ ] Database credentials changed in production
- [ ] CORS configured for specific domains
- [ ] Generated code isolated in `/generated_projects/`
- [ ] No code execution on generation
- [ ] Path traversal protection enabled
- [ ] Filename sanitization active
- [ ] HTTPS enabled in production

## Monitoring

### View System Status
```bash
docker-compose ps
docker stats
docker logs -f <container>
```

### Database Queries
```sql
-- Count projects
SELECT COUNT(*) FROM projects;

-- View by status
SELECT status, COUNT(*) FROM projects GROUP BY status;

-- Recent projects
SELECT * FROM projects ORDER BY created_at DESC LIMIT 10;

-- Failed projects
SELECT * FROM projects WHERE status = 'failed';
```

### API Metrics
- Check `/docs` for request counts
- View backend logs for timing
- Monitor database performance

## Useful Settings

### FastAPI Configuration
File: `backend/app/core/config.py`
```python
TEMPERATURE = 0.7          # Creativity level
MAX_TOKENS = 2000          # Response length
REQUEST_TIMEOUT = 300      # 5 minutes
```

### Ollama Configuration
```bash
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=deepseek-coder
```

### Frontend Configuration
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Extending the System

### Add New Agent
1. Create file: `backend/app/agents/my_agent.py`
2. Inherit from `BaseAgent`
3. Implement `execute()` method
4. Add to orchestrator

### Add New API Endpoint
1. Edit: `backend/app/api/routes.py`
2. Create route function
3. Add to router
4. Test at `/docs`

### Add New Component
1. Create file: `frontend/components/MyComponent.tsx`
2. Export component
3. Import in `app/page.tsx`
4. Use in layout

## Maintenance

### Regular Tasks
```bash
# Weekly
docker-compose logs --tail 1000 > backup.log  # Backup logs
du -sh generated_projects/  # Check disk usage

# Monthly
docker system prune  # Clean unused images
docker-compose restart  # Restart services

# Quarterly
docker-compose down -v  # Full reset if needed
Update dependencies
```

### Backup Generated Projects
```bash
# Backup
tar -czf projects_backup.tar.gz generated_projects/

# Restore
tar -xzf projects_backup.tar.gz
```

## Testing

### Manual Testing
1. Generate simple project
2. Check output files exist
3. Verify docker-compose.yml is valid
4. Check README is generated
5. Inspect generated code

### Automated Testing
```bash
# (Add pytest tests in future)
pytest backend/tests/
npm test  # in frontend
```

## Production Deployment

### Pre-deployment
- [ ] Test locally
- [ ] Update .env with production values
- [ ] Configure database backup
- [ ] Setup monitoring/logging
- [ ] Security audit completed

### Deployment
```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Deploy (example)
docker-compose -f docker-compose.prod.yml up -d

# Monitor
docker-compose logs -f
```

### Post-deployment
- [ ] Verify health endpoints
- [ ] Test main workflows
- [ ] Monitor resource usage
- [ ] Setup alerts

## Support & Documentation

- **README.md** - Features, tech stack, setup
- **STARTUP.md** - Detailed setup steps
- **ARCHITECTURE.md** - Technical design
- **PROJECT_STRUCTURE.md** - File listing
- **This file** - Quick reference

## Version Info

- **AutoDev-AI**: 1.0.0
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 15
- **Redis**: 7
- **Ollama**: Latest

---

**For full documentation, see README.md, STARTUP.md, and ARCHITECTURE.md**
