from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class TrainingResourceSchema(BaseModel):
    id: Optional[UUID] = None
    resource_name: str
    resource_type: str
    resource_url: str
    folder_name: Optional[str] = "General Resources"
    display_order: Optional[int] = 0

    class Config:
        from_attributes = True

class TrainingMaterialBase(BaseModel):
    title: str
    slug: Optional[str] = None
    short_description: str
    status: Optional[str] = "DRAFT"

class TrainingMaterialCreate(TrainingMaterialBase):
    resources: Optional[List[TrainingResourceSchema]] = []

class TrainingMaterialUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    short_description: Optional[str] = None
    status: Optional[str] = None
    resources: Optional[List[TrainingResourceSchema]] = None

class TrainingMaterialResponse(TrainingMaterialBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resources: Optional[List[TrainingResourceSchema]] = []

    class Config:
        from_attributes = True

class TrainingDownloadCreate(BaseModel):
    training_id: UUID
    resource_id: UUID

class TrainingDownloadResponse(BaseModel):
    id: UUID
    user_id: str
    training_id: UUID
    resource_id: UUID
    downloaded_at: datetime
    
    # Nested for easy rendering on frontend
    training: Optional[TrainingMaterialBase] = None
    resource: Optional[TrainingResourceSchema] = None

    class Config:
        from_attributes = True
