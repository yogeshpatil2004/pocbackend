from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class TrainingResource(Base):
    __tablename__ = "training_resources"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    training_id = Column(UUID(as_uuid=True), ForeignKey("training_materials.id", ondelete="CASCADE"))
    resource_name = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_url = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)

class TrainingMaterial(Base):
    __tablename__ = "training_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    short_description = Column(Text, nullable=False)
    status = Column(String, default="DRAFT") # DRAFT, PUBLISHED, ARCHIVED, DELETED
    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    resources = relationship("TrainingResource", cascade="all, delete-orphan")

class TrainingDownload(Base):
    __tablename__ = "training_downloads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    training_id = Column(UUID(as_uuid=True), ForeignKey("training_materials.id", ondelete="CASCADE"))
    resource_id = Column(UUID(as_uuid=True), ForeignKey("training_resources.id", ondelete="CASCADE"))
    downloaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    training = relationship("TrainingMaterial")
    resource = relationship("TrainingResource")
