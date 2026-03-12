import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID

from app.models.project import Project, ProjectStatus
from app.agents.requirement_agent import RequirementAgent
from app.agents.architecture_agent import ArchitectureAgent
from app.agents.backend_agent import BackendAgent
from app.agents.frontend_agent import FrontendAgent
from app.agents.devops_agent import DevOpsAgent
from app.services.project_builder import ProjectBuilder

logger = logging.getLogger(__name__)


class ProjectOrchestrator:
    """Orchestrates the code generation pipeline"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.requirement_agent = RequirementAgent()
        self.architecture_agent = ArchitectureAgent()
        self.backend_agent = BackendAgent()
        self.frontend_agent = FrontendAgent()
        self.devops_agent = DevOpsAgent()
        self.builder = ProjectBuilder()

    async def generate_project(self, project_id: UUID, prompt: str) -> bool:
        """Execute full project generation pipeline"""
        try:
            # Update status
            await self._update_project_status(project_id, ProjectStatus.ANALYZING)

            # Step 1: Analyze requirements
            logger.info(f"[{project_id}] Analyzing requirements...")
            requirements = await self.requirement_agent.execute({"prompt": prompt})
            logger.info(f"[{project_id}] Requirements: {requirements}")

            # Step 2: Plan architecture
            logger.info(f"[{project_id}] Planning architecture...")
            architecture = await self.architecture_agent.execute(
                {"requirements": requirements}
            )
            logger.info(f"[{project_id}] Architecture planned")

            # Step 3: Generate backend
            await self._update_project_status(project_id, ProjectStatus.GENERATING_BACKEND)
            logger.info(f"[{project_id}] Generating backend...")
            backend_code = await self.backend_agent.execute(
                {"requirements": requirements, "architecture": architecture}
            )
            logger.info(f"[{project_id}] Backend generated")

            # Step 4: Generate frontend
            await self._update_project_status(project_id, ProjectStatus.GENERATING_FRONTEND)
            logger.info(f"[{project_id}] Generating frontend...")
            frontend_code = await self.frontend_agent.execute(
                {"requirements": requirements, "architecture": architecture}
            )
            logger.info(f"[{project_id}] Frontend generated")

            # Step 5: Generate DevOps
            await self._update_project_status(project_id, ProjectStatus.DOCKERIZING)
            logger.info(f"[{project_id}] Generating DevOps configuration...")
            devops_config = await self.devops_agent.execute(
                {"requirements": requirements}
            )
            logger.info(f"[{project_id}] DevOps configured")

            # Step 6: Build project structure
            logger.info(f"[{project_id}] Building project structure...")
            output_path = await self.builder.build_project(
                project_id=str(project_id),
                requirements=requirements,
                backend_code=backend_code,
                frontend_code=frontend_code,
                devops_config=devops_config,
            )
            logger.info(f"[{project_id}] Project structure built")

            # Mark as completed
            await self._update_project_status(
                project_id, ProjectStatus.COMPLETED, output_path=output_path
            )

            logger.info(f"[{project_id}] Project generation completed successfully")
            return True

        except Exception as e:
            logger.error(f"[{project_id}] Project generation failed: {str(e)}", exc_info=True)
            await self._update_project_status(
                project_id, ProjectStatus.FAILED, error=str(e)
            )
            return False

    async def _update_project_status(
        self,
        project_id: UUID,
        status: ProjectStatus,
        output_path: Optional[str] = None,
        error: Optional[str] = None,
    ):
        """Update project status in database"""
        try:
            stmt = (
                update(Project)
                .where(Project.id == project_id)
                .values(status=status, error_message=error, output_path=output_path)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            logger.info(f"[{project_id}] Status updated to {status}")
        except Exception as e:
            logger.error(f"[{project_id}] Failed to update status: {str(e)}")
