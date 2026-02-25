from typing import Dict, Any
from app.agents.base import BaseAgent


class RequirementAgent(BaseAgent):
    """Analyzes user prompt and extracts requirements"""

    def __init__(self):
        super().__init__("RequirementAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract requirements from user prompt"""
        prompt = input_data.get("prompt", "")
        
        self.log_execution(f"Analyzing prompt: {prompt[:100]}...")

        schema = """{
            "project_name": "string",
            "project_description": "string",
            "features": ["string"],
            "tech_stack": {
                "backend": "string",
                "frontend": "string",
                "database": "string"
            },
            "complexity": "simple|medium|complex",
            "authentication_required": "boolean",
            "realtime_features": "boolean"
        }"""

        system_prompt = """You are an expert system architect. Analyze the user requirement and extract structured information.
        Be specific about features, technology choices, and complexity level."""

        analysis_prompt = f"""Analyze this project requirement and provide structured output:

User Requirement: {prompt}

Extract the project name, description, features list, recommended tech stack, complexity level, and whether authentication or real-time features are needed."""

        result = await self.call_ollama_json(
            prompt=analysis_prompt,
            schema=schema,
            system_prompt=system_prompt,
            temperature=0.3,
        )

        self.log_execution("Requirement analysis completed")
        return result
