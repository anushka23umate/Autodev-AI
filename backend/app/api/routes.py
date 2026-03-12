import logging
import asyncio
import zipfile
import io
from pathlib import Path
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.database import get_db
from app.core.config import settings
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectStatusUpdate
from app.services.orchestrator import ProjectOrchestrator
from app.utils.path_utils import get_project_path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["projects"])


@router.post("/generate", response_model=ProjectResponse)
async def generate_project(
    request: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new code generation project
    """
    try:
        # Create project record
        project = Project(
            name=request.prompt[:50],
            prompt=request.prompt,
            description=request.prompt[:200],
            status=ProjectStatus.QUEUED,
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)

        # Add orchestration task
        background_tasks.add_task(
            _run_orchestration,
            project_id=project.id,
            prompt=request.prompt,
        )

        logger.info(f"Project {project.id} created and queued for generation")
        return ProjectResponse.from_orm(project)

    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get project status and information
    """
    try:
        stmt = select(Project).where(Project.id == project_id)
        result = await db.execute(stmt)
        project = result.scalars().first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return ProjectResponse.from_orm(project)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/download")
async def download_project_zip(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Download the generated project as a ZIP file. Only available when status is completed.
    """
    try:
        stmt = select(Project).where(Project.id == project_id)
        result = await db.execute(stmt)
        project = result.scalars().first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.status != ProjectStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="Project is not ready for download. Generation must complete first.",
            )

        project_path = get_project_path(str(project_id))
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project files not found")

        # Build zip in memory
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in project_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(project_path)
                    zf.write(file_path, arcname)

        buffer.seek(0)
        filename = f"project-{project_id}.zip"
        return StreamingResponse(
            buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating project zip: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects")
async def list_projects(
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    """
    List all projects with pagination
    """
    try:
        stmt = select(Project).offset(offset).limit(limit).order_by(Project.created_at.desc())
        result = await db.execute(stmt)
        projects = result.scalars().all()

        return {
            "projects": [ProjectResponse.from_orm(p) for p in projects],
            "total": len(projects),
        }

    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _run_orchestration(project_id: UUID, prompt: str):
    """
    Background task for project orchestration
    """
    logger.info(f"Starting orchestration for project {project_id}")
    
    # Create a new database session for the background task
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )
    
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
    )
    
    async with async_session_maker() as db:
        try:
            orchestrator = ProjectOrchestrator(db)
            await orchestrator.generate_project(project_id, prompt)
        except Exception as e:
            logger.error(f"Orchestration failed for {project_id}: {str(e)}")
        finally:
            await engine.dispose()
