from typing import Dict, Any
from app.agents.base import BaseAgent


class ArchitectureAgent(BaseAgent):
    """Plans application architecture based on requirements"""

    def __init__(self):
        super().__init__("ArchitectureAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create architecture plan"""
        requirements = input_data.get("requirements", {})
        
        self.log_execution("Planning application architecture...")

        schema = """{
            "api_endpoints": [{"path": "string", "method": "string", "description": "string"}],
            "database_schema": [{"name": "string", "fields": [{"name": "string", "type": "string"}]}],
            "frontend_pages": [{"name": "string", "path": "string", "components": ["string"]}],
            "deployment_strategy": "docker|kubernetes",
            "security_considerations": ["string"],
            "scalability_approach": "string"
        }"""

        system_prompt = """You are a senior software architect. Design a scalable, production-ready architecture."""

        arch_prompt = f"""Based on these requirements, design the application architecture:

Requirements: {str(requirements)}

Provide API endpoints, database schema, frontend pages, deployment strategy, security considerations, and scalability approach."""

        result = await self.call_ollama_json(
            prompt=arch_prompt,
            schema=schema,
            system_prompt=system_prompt,
            temperature=0.3,
        )

        self.log_execution("Architecture planning completed")
        return result
