from typing import Dict, Any
from app.agents.base import BaseAgent


class DevOpsAgent(BaseAgent):
    """Generates DevOps configuration"""

    def __init__(self):
        super().__init__("DevOpsAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate DevOps configuration"""
        requirements = input_data.get("requirements", {})
        
        self.log_execution("Generating DevOps configuration...")

        system_prompt = """You are an expert DevOps engineer. Generate production-ready Docker and deployment configurations."""

        backend_dockerfile_prompt = f"""Generate a Dockerfile for a FastAPI backend with:

Requirements: {str(requirements)}

Use Python 3.11 slim image, proper multi-stage build, and security best practices."""

        backend_dockerfile = await self.call_ollama(
            prompt=backend_dockerfile_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        frontend_dockerfile_prompt = f"""Generate a Dockerfile for a Next.js frontend:

Requirements: {str(requirements)}

Use node:18 alpine for multi-stage build, optimize bundle size."""

        frontend_dockerfile = await self.call_ollama(
            prompt=frontend_dockerfile_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        compose_prompt = f"""Generate a docker-compose.yml for this full stack application:

Requirements: {str(requirements)}

Include: backend, frontend, PostgreSQL, Redis services. Use environment variables, volumes, and health checks."""

        docker_compose = await self.call_ollama(
            prompt=compose_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        readme_prompt = f"""Generate a comprehensive README.md with:

Requirements: {str(requirements)}

Include: overview, tech stack, installation, setup, running locally, Docker setup, API docs, and deployment."""

        readme = await self.call_ollama(
            prompt=readme_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        self.log_execution("DevOps configuration generation completed")
        return {
            "backend_dockerfile": backend_dockerfile,
            "frontend_dockerfile": frontend_dockerfile,
            "docker_compose": docker_compose,
            "readme": readme,
        }
