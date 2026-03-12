import logging
from typing import Dict, Any
from pathlib import Path

from app.utils.path_utils import create_project_structure, write_file_safely
from app.core.config import settings

logger = logging.getLogger(__name__)


class ProjectBuilder:
    """Builds project directory structure and writes files"""

    async def build_project(
        self,
        project_id: str,
        requirements: Dict[str, Any],
        backend_code: Dict[str, Any],
        frontend_code: Dict[str, Any],
        devops_config: Dict[str, Any],
    ) -> str:
        """Build complete project structure"""
        
        project_name = requirements.get("project_name", "generated-app")
        dirs = create_project_structure(project_id)

        # Write backend files
        await self._write_backend_files(
            project_id, dirs, backend_code, requirements
        )

        # Write frontend files
        await self._write_frontend_files(
            project_id, dirs, frontend_code
        )

        # Write DevOps files
        await self._write_devops_files(
            project_id, dirs, devops_config
        )

        # Write .env.example
        await self._write_env_file(project_id, dirs)

        project_path = Path(settings.PROJECTS_BASE_PATH) / project_id
        return str(project_path)

    async def _write_backend_files(
        self,
        project_id: str,
        dirs: Dict[str, str],
        backend_code: Dict[str, Any],
        requirements: Dict[str, Any],
    ):
        """Write backend files"""
        
        # main.py
        main_py = backend_code.get("main_py", self._get_default_main_py())
        write_file_safely(
            f"{dirs['backend_app']}/main.py",
            main_py
        )

        # models.py
        models_py = backend_code.get("models_py", self._get_default_models_py())
        write_file_safely(
            f"{dirs['backend_app']}/models.py",
            models_py
        )

        # routes.py
        routes_py = backend_code.get("routes_py", self._get_default_routes_py())
        write_file_safely(
            f"{dirs['backend_app']}/routes.py",
            routes_py
        )

        # requirements.txt
        requirements_txt = self._generate_requirements_txt(requirements)
        write_file_safely(
            f"{dirs['backend']}/requirements.txt",
            requirements_txt
        )

        # __init__.py
        write_file_safely(f"{dirs['backend_app']}/__init__.py", "")

        logger.info(f"[{project_id}] Backend files written")

    async def _write_frontend_files(
        self,
        project_id: str,
        dirs: Dict[str, str],
        frontend_code: Dict[str, Any],
    ):
        """Write frontend files"""
        
        # layout.tsx
        layout_tsx = frontend_code.get("layout_tsx", self._get_default_layout())
        write_file_safely(
            f"{dirs['frontend_app']}/layout.tsx",
            layout_tsx
        )

        # page.tsx
        page_tsx = frontend_code.get("page_tsx", self._get_default_page())
        write_file_safely(
            f"{dirs['frontend_app']}/page.tsx",
            page_tsx
        )

        # globals.css
        write_file_safely(
            f"{dirs['frontend_app']}/globals.css",
            self._get_default_globals_css()
        )

        # API service
        api_service = frontend_code.get("api_service", self._get_default_api_service())
        write_file_safely(
            f"{dirs['frontend']}/services/api.ts",
            api_service
        )

        # package.json
        package_json = self._generate_package_json()
        write_file_safely(
            f"{dirs['frontend']}/package.json",
            package_json
        )

        # next.config.js
        write_file_safely(
            f"{dirs['frontend']}/next.config.js",
            self._get_default_next_config()
        )

        # tailwind.config.ts
        write_file_safely(
            f"{dirs['frontend']}/tailwind.config.ts",
            self._get_default_tailwind_config()
        )

        # tsconfig.json
        write_file_safely(
            f"{dirs['frontend']}/tsconfig.json",
            self._get_default_tsconfig()
        )

        logger.info(f"[{project_id}] Frontend files written")

    async def _write_devops_files(
        self,
        project_id: str,
        dirs: Dict[str, str],
        devops_config: Dict[str, Any],
    ):
        """Write DevOps configuration files"""
        
        project_path = Path(dirs['backend']).parent

        # Backend Dockerfile
        backend_dockerfile = devops_config.get(
            "backend_dockerfile", self._get_default_backend_dockerfile()
        )
        write_file_safely(
            f"{dirs['backend']}/Dockerfile",
            backend_dockerfile
        )

        # Frontend Dockerfile
        frontend_dockerfile = devops_config.get(
            "frontend_dockerfile", self._get_default_frontend_dockerfile()
        )
        write_file_safely(
            f"{dirs['frontend']}/Dockerfile",
            frontend_dockerfile
        )

        # docker-compose.yml
        docker_compose = devops_config.get(
            "docker_compose", self._get_default_docker_compose()
        )
        write_file_safely(
            f"{str(project_path)}/docker-compose.yml",
            docker_compose
        )

        # README.md
        readme = devops_config.get("readme", self._get_default_readme())
        write_file_safely(
            f"{str(project_path)}/README.md",
            readme
        )

        logger.info(f"[{project_id}] DevOps files written")

    async def _write_env_file(self, project_id: str, dirs: Dict[str, str]):
        """Write .env.example file"""
        env_content = self._get_default_env_example()
        project_path = Path(dirs['backend']).parent
        write_file_safely(
            f"{str(project_path)}/.env.example",
            env_content
        )

    def _generate_requirements_txt(self, requirements: Dict[str, Any]) -> str:
        """Generate requirements.txt"""
        return """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
redis==5.0.1
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.1
"""

    def _generate_package_json(self) -> str:
        """Generate package.json"""
        return """{
  "name": "autodev-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0",
    "axios": "^1.6.2",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@types/node": "^20.10.0"
  }
}
"""

    def _get_default_main_py(self) -> str:
        return """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Generated API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
"""

    def _get_default_models_py(self) -> str:
        return """from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

    def _get_default_routes_py(self) -> str:
        return """from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
async def get_items():
    return {"items": []}

@router.post("/items")
async def create_item(title: str, description: str = None):
    return {"id": "1", "title": title, "description": description}
"""

    def _get_default_layout(self) -> str:
        return """import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Generated App',
  description: 'Generated with AutoDev-AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
"""

    def _get_default_page(self) -> str:
        return """'use client'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-indigo-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Your Generated App
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Built with AutoDev-AI
        </p>
        <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
          Get Started
        </button>
      </div>
    </div>
  )
}
"""

    def _get_default_api_service(self) -> str:
        return """import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  get: (url: string) => apiClient.get(url),
  post: (url: string, data: any) => apiClient.post(url, data),
  put: (url: string, data: any) => apiClient.put(url, data),
  delete: (url: string) => apiClient.delete(url),
}
"""

    def _get_default_globals_css(self) -> str:
        return """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
}
"""

    def _get_default_next_config(self) -> str:
        return """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
}

module.exports = nextConfig
"""

    def _get_default_tailwind_config(self) -> str:
        return """import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
export default config
"""

    def _get_default_tsconfig(self) -> str:
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitThis": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["app", "components"],
  "exclude": ["node_modules"]
}
"""

    def _get_default_backend_dockerfile(self) -> str:
        return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _get_default_frontend_dockerfile(self) -> str:
        return """FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
"""

    def _get_default_docker_compose(self) -> str:
        return """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: autodev-postgres
    environment:
      POSTGRES_USER: autodev
      POSTGRES_PASSWORD: autodev
      POSTGRES_DB: autodev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U autodev"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: autodev-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: autodev-backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://autodev:autodev@postgres:5432/autodev
      REDIS_URL: redis://redis:6379/0
      OLLAMA_BASE_URL: http://ollama:11434
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - autodev-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: autodev-frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000/api
    depends_on:
      - backend
    networks:
      - autodev-network

volumes:
  postgres_data:

networks:
  autodev-network:
    driver: bridge
"""

    def _get_default_readme(self) -> str:
        return """# Generated Project

This project was generated by AutoDev-AI.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14 with React 18
- **Database**: PostgreSQL
- **Cache**: Redis
- **Infrastructure**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Ollama running locally

### Setup

1. Clone the repository
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

3. Start services:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
.
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docker-compose.yml
└── README.md
```

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `.env.example` for all available configuration options.

## API Documentation

FastAPI automatically generates interactive API documentation at `/docs`

## License

MIT
"""

    def _get_default_env_example(self) -> str:
        return """# Database
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
"""
