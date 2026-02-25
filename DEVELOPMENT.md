# AutoDev-AI - Development Guide

## Development Environment Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Ollama
- Git

### Backend Development

```bash
# Clone and setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-asyncio black isort mypy pylint

# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Clone and setup
cd frontend
npm install

# Install development tools
npm install --save-dev eslint prettier typescript

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## Code Structure

### Backend Architecture

```
app/
├── main.py                 # Entry point - configure FastAPI
├── api/
│   └── routes.py          # HTTP endpoints
├── agents/
│   ├── base.py            # Abstract base agent
│   └── *_agent.py         # Specialized agents
├── core/
│   ├── config.py          # Settings management
│   └── database.py        # Database initialization
├── models/
│   └── project.py         # SQLAlchemy models
├── schemas/
│   └── project.py         # Pydantic schemas
├── services/
│   ├── ollama_service.py  # LLM integration
│   ├── orchestrator.py    # Pipeline coordination
│   └── project_builder.py # File generation
└── utils/
    ├── path_utils.py      # Path validation
    └── code_generator.py  # Code formatting
```

### Key Design Patterns

#### 1. Agent Pattern
Each agent is a self-contained module:
```python
class MyAgent(BaseAgent):
    async def execute(self, input_data: Dict) -> Dict:
        # 1. Prepare prompt
        # 2. Call Ollama
        # 3. Parse response
        # 4. Return structured data
```

#### 2. Service Layer
Services handle business logic:
```python
class MyService:
    def __init__(self):
        self.dependency = ...
    
    async def do_something(self, data):
        # Main logic
        pass
```

#### 3. Dependency Injection
FastAPI provides dependencies:
```python
@router.get("/path")
async def endpoint(db: AsyncSession = Depends(get_db)):
    # db is automatically provided
```

## Adding Features

### Adding a New Agent

1. **Create agent file**: `backend/app/agents/my_agent.py`

```python
from app.agents.base import BaseAgent
from typing import Dict, Any

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.log_execution("Starting...")
        
        prompt = f"Your prompt here: {input_data.get('key')}"
        schema = "{...json schema...}"
        
        result = await self.call_ollama_json(
            prompt=prompt,
            schema=schema,
            temperature=0.3
        )
        
        self.log_execution("Completed")
        return result
```

2. **Add to orchestrator**: `backend/app/services/orchestrator.py`

```python
from app.agents.my_agent import MyAgent

class ProjectOrchestrator:
    def __init__(self, db):
        self.my_agent = MyAgent()
    
    async def generate_project(self, project_id, prompt):
        # ... existing code ...
        my_result = await self.my_agent.execute({...})
        # Use my_result
```

### Adding an API Endpoint

1. **Add to routes**: `backend/app/api/routes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

@router.post("/api/my-endpoint")
async def my_endpoint(
    request: MyRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    My endpoint description.
    """
    try:
        # Implementation
        result = await do_something(request)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

2. **Add request schema**: `backend/app/schemas/project.py`

```python
from pydantic import BaseModel, Field

class MyRequest(BaseModel):
    field1: str = Field(..., min_length=1, max_length=100)
    field2: int = Field(default=10, ge=0)

class MyResponse(BaseModel):
    status: str
    data: Dict[str, Any]
```

### Adding a Frontend Component

1. **Create component**: `frontend/components/MyComponent.tsx`

```typescript
'use client'

import { useState, useEffect } from 'react'
import { api } from '@/services/api'

interface MyComponentProps {
  title: string
}

export default function MyComponent({ title }: MyComponentProps) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const response = await api.get('/endpoint')
        setData(response.data)
      } catch (error) {
        console.error(error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])
  
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">{title}</h2>
      {loading && <p>Loading...</p>}
      {data && <p>{JSON.stringify(data)}</p>}
    </div>
  )
}
```

2. **Use in page**: `frontend/app/page.tsx`

```typescript
import MyComponent from '@/components/MyComponent'

export default function Home() {
  return (
    <div>
      <MyComponent title="My Title" />
    </div>
  )
}
```

## Testing

### Backend Tests

```python
# backend/tests/test_routes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_generate_project():
    # Test implementation
    pass
```

### Frontend Tests

```typescript
// frontend/__tests__/components.test.tsx
import { render, screen } from '@testing-library/react'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" />)
    expect(screen.getByText('Test')).toBeInTheDocument()
  })
})
```

## Debugging

### Backend Debugging

```python
# Using print statements
print(f"Debug: {variable}")

# Using logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Debug message: {data}")

# Using debugger
import pdb; pdb.set_trace()
```

### Frontend Debugging

```typescript
// Browser console
console.log('Debug:', variable)
console.error('Error:', error)

// React DevTools Chrome extension
// Network tab for API debugging

// VS Code debugging
// Add breakpoints and use debugger
```

### Docker Debugging

```bash
# View logs
docker-compose logs -f <service>

# Interactive shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Inspect container
docker inspect <container_id>
```

## Code Style

### Python (Backend)

```bash
# Format code
black backend/

# Sort imports
isort backend/

# Lint
pylint backend/

# Type checking
mypy backend/
```

### TypeScript (Frontend)

```bash
# Format code
npx prettier --write .

# Lint
npx eslint .

# Type check
npm run type-check
```

## Performance Optimization

### Backend

1. **Database Queries**
   - Use SELECT * sparingly
   - Add database indexes
   - Use connection pooling

2. **Async/Await**
   - Always await async calls
   - Use gather() for parallel tasks
   ```python
   import asyncio
   results = await asyncio.gather(task1(), task2())
   ```

3. **Caching**
   ```python
   from functools import lru_cache
   @lru_cache(maxsize=128)
   def expensive_function(param):
       return result
   ```

### Frontend

1. **Component Optimization**
   ```typescript
   import { memo } from 'react'
   
   const MyComponent = memo(function MyComponent(props) {
     return <div>{props.children}</div>
   })
   ```

2. **Image Optimization**
   ```typescript
   import Image from 'next/image'
   
   <Image
     src="/image.jpg"
     alt="Description"
     width={400}
     height={300}
   />
   ```

## Security Best Practices

### Backend

1. **Input Validation**
   ```python
   from pydantic import BaseModel, Field, validator
   
   class Request(BaseModel):
       name: str = Field(..., min_length=1, max_length=100)
       
       @validator('name')
       def name_must_not_contain_special(cls, v):
           if any(c in v for c in ['<', '>', '&']):
               raise ValueError('Invalid characters')
           return v
   ```

2. **Path Traversal Protection**
   ```python
   from pathlib import Path
   
   def safe_path(user_input):
       base = Path('/safe/base')
       target = (base / user_input).resolve()
       target.relative_to(base.resolve())  # Raises if traversal
       return target
   ```

3. **Environment Secrets**
   ```python
   import os
   secret = os.getenv('SECRET_KEY')
   # Never commit secrets to git
   ```

### Frontend

1. **Sanitize User Input**
   ```typescript
   import DOMPurify from 'isomorphic-dompurify'
   
   const clean = DOMPurify.sanitize(userInput)
   ```

2. **Environment Variables**
   ```env
   # Only public variables (prefixed with NEXT_PUBLIC_)
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Documentation

### Code Comments
```python
def complex_function(param1, param2):
    """
    Summary of what this function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is wrong
    """
    pass
```

### Docstrings
```typescript
/**
 * Fetches user data from the API.
 * @param userId - The user ID
 * @returns The user data
 */
async function getUser(userId: string): Promise<User> {
  // Implementation
}
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: description of change"

# Push and create PR
git push origin feature/my-feature

# Update main
git checkout main
git pull
git merge feature/my-feature
git push
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Continuous Integration

### Pre-commit Checks
```bash
# Run tests
pytest backend/
npm test

# Code quality
black --check backend/
mypy backend/
npx eslint frontend/
```

## Deployment

### Building for Production

```bash
# Backend
docker build -f backend/Dockerfile -t autodev-backend:1.0.0 backend/

# Frontend
docker build -f frontend/Dockerfile -t autodev-frontend:1.0.0 frontend/

# Push to registry
docker tag autodev-backend:1.0.0 registry/autodev-backend:1.0.0
docker push registry/autodev-backend:1.0.0
```

### Environment Setup

```env
# Production .env
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/prod_db
OLLAMA_BASE_URL=http://prod-ollama:11434
ENVIRONMENT=production
DEBUG=False
```

## Monitoring & Metrics

### Backend Metrics
- API response times
- Database query performance
- Error rates
- Ollama latency

### Frontend Metrics
- Page load time
- Time to interactive
- Core Web Vitals
- Error tracking

## Troubleshooting Development

### "ModuleNotFoundError"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Clear cache
rm -rf __pycache__
```

### "npm ERR!"
```bash
# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

### "Port already in use"
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

---

**For more information, see README.md and ARCHITECTURE.md**
