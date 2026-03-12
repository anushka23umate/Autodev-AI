import os
import re
from pathlib import Path
from app.core.config import settings


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from filename"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:255]


def get_project_path(project_id: str) -> Path:
    """Get project directory path with validation"""
    base_path = Path(settings.PROJECTS_BASE_PATH)
    base_path.mkdir(parents=True, exist_ok=True)
    
    project_path = base_path / str(project_id)
    
    # Ensure path is within base_path
    try:
        project_path.resolve().relative_to(base_path.resolve())
    except ValueError:
        raise ValueError("Path traversal detected")
    
    return project_path


def create_project_structure(project_id: str) -> dict:
    """Create project directory structure"""
    project_path = get_project_path(project_id)
    project_path.mkdir(parents=True, exist_ok=True)
    
    dirs = {
        "backend": project_path / "backend",
        "backend_app": project_path / "backend" / "app",
        "frontend": project_path / "frontend",
        "frontend_app": project_path / "frontend" / "app",
        "frontend_components": project_path / "frontend" / "components",
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return {k: str(v) for k, v in dirs.items()}


def write_file_safely(file_path: str, content: str) -> bool:
    """Write file with path traversal protection"""
    base_path = Path(settings.PROJECTS_BASE_PATH)
    target_path = Path(file_path).resolve()
    
    try:
        target_path.relative_to(base_path.resolve())
    except ValueError:
        raise ValueError("Path traversal detected")
    
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True
