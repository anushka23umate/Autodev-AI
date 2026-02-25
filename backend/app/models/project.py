import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base


class ProjectStatus(str, enum.Enum):
    QUEUED = "queued"
    ANALYZING = "analyzing"
    GENERATING_BACKEND = "generating_backend"
    GENERATING_FRONTEND = "generating_frontend"
    DOCKERIZING = "dockerizing"
    COMPLETED = "completed"
    FAILED = "failed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.QUEUED)
    output_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Project {self.id} - {self.name} - {self.status}>"
