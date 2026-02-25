from typing import Dict, Any
from app.agents.base import BaseAgent


class FrontendAgent(BaseAgent):
    """Generates frontend code"""

    def __init__(self):
        super().__init__("FrontendAgent")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate frontend code"""
        requirements = input_data.get("requirements", {})
        architecture = input_data.get("architecture", {})
        
        self.log_execution("Generating frontend code...")

        system_prompt = """You are an expert Next.js/React developer. Generate production-ready code using TypeScript and Tailwind CSS."""

        layout_prompt = f"""Generate a Next.js layout.tsx (App Router) for:

Requirements: {str(requirements)}
Frontend Pages: {str(architecture.get('frontend_pages', []))}

Include Tailwind CSS styling, proper metadata, and provider setup."""

        layout_tsx = await self.call_ollama(
            prompt=layout_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        page_prompt = f"""Generate a main page.tsx component for the home page with:

Requirements: {str(requirements)}

Include interactive elements, Tailwind styling, and proper TypeScript types."""

        page_tsx = await self.call_ollama(
            prompt=page_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        components_prompt = f"""Generate React components for:

Frontend Pages: {str(architecture.get('frontend_pages', []))}

Use TypeScript, Tailwind CSS, and include proper prop types."""

        components_tsx = await self.call_ollama(
            prompt=components_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        services_prompt = f"""Generate API service class for calling these endpoints:

API Endpoints: {str(architecture.get('api_endpoints', []))}

Use Axios, proper error handling, and TypeScript types."""

        api_service = await self.call_ollama(
            prompt=services_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
        )

        self.log_execution("Frontend code generation completed")
        return {
            "layout_tsx": layout_tsx,
            "page_tsx": page_tsx,
            "components_tsx": components_tsx,
            "api_service": api_service,
        }
