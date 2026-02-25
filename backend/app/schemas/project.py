from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000)


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    prompt: str
    status: str
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectStatusUpdate(BaseModel):
    status: str
    error_message: Optional[str] = None
