from fastapi import APIRouter
from app.schemas.poc import SettingsBase
from app.services import poc_service

router = APIRouter()

@router.get("/settings", response_model=SettingsBase)
async def get_settings():
    """Retrieve global website branding and settings."""
    return poc_service.SETTINGS_REPOSITORY

@router.put("/settings", response_model=SettingsBase)
async def update_settings(payload: SettingsBase):
    """Admin endpoint: Update website settings."""
    poc_service.SETTINGS_REPOSITORY.update(payload.model_dump(exclude_unset=True))
    return poc_service.SETTINGS_REPOSITORY
