from typing import Dict, Any
from app.agents.base import BaseAgent


class BackendAgent(BaseAgent):
    """Generates backend code"""

    def __init__(self):
        super().__init__("BackendAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate backend code"""
        requirements = input_data.get("requirements", {})
        architecture = input_data.get("architecture", {})
        
        self.log_execution("Generating backend code...")

        system_prompt = """You are an expert Python/FastAPI developer. Generate production-ready code."""

        main_py_prompt = f"""Generate a complete FastAPI main.py for this application:

Requirements: {str(requirements)}
Architecture: {str(architecture)}

Include:
- FastAPI app setup
- CORS middleware
- Database configuration
- Error handling
- Health check endpoint"""

        main_py = await self.call_ollama(
            prompt=main_py_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        models_prompt = f"""Generate SQLAlchemy models for these database tables:

Database Schema: {str(architecture.get('database_schema', []))}

Use Pydantic for validation, proper relationships, and timestamps."""

        models_py = await self.call_ollama(
            prompt=models_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        routes_prompt = f"""Generate FastAPI routes for these endpoints:

API Endpoints: {str(architecture.get('api_endpoints', []))}

Include proper error handling, validation, and documentation."""

        routes_py = await self.call_ollama(
            prompt=routes_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        self.log_execution("Backend code generation completed")
        return {
            "main_py": main_py,
            "models_py": models_py,
            "routes_py": routes_py,
        }
