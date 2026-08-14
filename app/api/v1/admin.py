from fastapi import APIRouter
from app.services import poc_service

router = APIRouter()

@router.get("/admin/analytics")
async def get_analytics():
    """Retrieve full dashboard telemetry (Total, Published, Drafts, Soft-Deleted, Views)."""
    return await poc_service.get_analytics_summary()
