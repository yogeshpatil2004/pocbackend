from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.training import (
    TrainingMaterialCreate, TrainingMaterialUpdate, TrainingMaterialResponse, 
    TrainingDownloadCreate, TrainingDownloadResponse, TrainingFolderCreate, 
    TrainingFolderResponse, FolderContentResponse, TrainingResourceSchema
)
from app.services import training_service
from app.db.session import get_db
from app.core.security import verify_clerk_token

router = APIRouter()

@router.get("/training/explorer/contents", response_model=FolderContentResponse)
async def get_explorer_contents(
    folder_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await training_service.get_folder_contents(db, folder_id)

@router.post("/training/folders", response_model=TrainingFolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    payload: TrainingFolderCreate,
    db: AsyncSession = Depends(get_db)
):
    return await training_service.create_folder(db, payload.name, str(payload.parent_id) if payload.parent_id else None)

@router.delete("/training/folders/{folder_id}")
async def delete_folder(
    folder_id: str,
    db: AsyncSession = Depends(get_db)
):
    success = await training_service.delete_folder(db, folder_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Folder ID {folder_id} not found")
    return {"message": "Folder deleted successfully"}

@router.post("/training/resources", response_model=TrainingResourceSchema, status_code=status.HTTP_201_CREATED)
async def create_standalone_resource(
    payload: TrainingResourceSchema,
    db: AsyncSession = Depends(get_db)
):
    data = payload.model_dump()
    data["folder_id"] = str(payload.folder_id) if payload.folder_id else None
    data["training_id"] = str(payload.training_id) if payload.training_id else None
    return await training_service.create_standalone_resource(db, data)

@router.delete("/training/resources/{resource_id}")
async def delete_standalone_resource(
    resource_id: str,
    db: AsyncSession = Depends(get_db)
):
    success = await training_service.delete_standalone_resource(db, resource_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Resource ID {resource_id} not found")
    return {"message": "Resource deleted successfully"}

@router.post("/training/downloads", status_code=status.HTTP_201_CREATED)
async def record_download(
    payload: TrainingDownloadCreate, 
    db: AsyncSession = Depends(get_db),
    token_payload: dict = Depends(verify_clerk_token)
):
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
        
    await training_service.record_download(
        db, 
        user_id=user_id, 
        training_id=str(payload.training_id) if payload.training_id else None, 
        resource_id=str(payload.resource_id)
    )
    return {"status": "success"}

@router.get("/training/downloads/history", response_model=List[TrainingDownloadResponse])
async def get_downloads(
    db: AsyncSession = Depends(get_db),
    token_payload: dict = Depends(verify_clerk_token)
):
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
        
    return await training_service.get_user_downloads(db, user_id)

@router.get("/training", response_model=List[TrainingMaterialResponse])
async def list_trainings(
    status: Optional[str] = Query("PUBLISHED"),
    search: Optional[str] = Query(None),
    include_deleted: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    return await training_service.get_trainings(
        db, status, search, include_deleted
    )

@router.get("/training/{identifier}", response_model=TrainingMaterialResponse)
async def get_training(identifier: str, db: AsyncSession = Depends(get_db)):
    training = await training_service.get_training_by_id_or_slug(db, identifier)
    if not training:
        raise HTTPException(status_code=404, detail=f"Training '{identifier}' not found")
    return training

@router.post("/training", response_model=TrainingMaterialResponse, status_code=status.HTTP_201_CREATED)
async def create_training(payload: TrainingMaterialCreate, db: AsyncSession = Depends(get_db)):
    return await training_service.create_training(db, payload)

@router.put("/training/{training_id}", response_model=TrainingMaterialResponse)
async def update_training(training_id: str, payload: TrainingMaterialUpdate, db: AsyncSession = Depends(get_db)):
    updated = await training_service.update_training(db, training_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Training ID {training_id} not found")
    return updated

@router.delete("/training/{training_id}")
async def delete_training(training_id: str, db: AsyncSession = Depends(get_db)):
    success = await training_service.delete_training(db, training_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Training ID {training_id} not found")
    return {"message": f"Training {training_id} moved to DELETED status successfully"}
