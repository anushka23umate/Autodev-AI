import logging
import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.services.ollama_service import ollama_service

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, name: str):
        self.name = name
        self.ollama = ollama_service

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic - must be implemented by subclasses"""
        pass

    async def call_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Call Ollama with custom prompt"""
        return await self.ollama.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )

    async def call_ollama_json(
        self,
        prompt: str,
        schema: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        """Call Ollama expecting JSON response"""
        return await self.ollama.generate_json(
            prompt=prompt,
            schema=schema,
            system_prompt=system_prompt,
            temperature=temperature,
        )

    def log_execution(self, message: str):
        """Log agent execution"""
        logger.info(f"[{self.name}] {message}")
