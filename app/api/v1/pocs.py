from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List, Optional
from app.schemas.poc import POCCreate, POCUpdate, POCResponse
from app.services import poc_service

router = APIRouter()

@router.get("/pocs", response_model=List[POCResponse])
async def list_pocs(
    status: Optional[str] = Query("PUBLISHED"),
    category_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    include_deleted: bool = Query(False)
):
    """Public & Admin API listing POCs with optional status, category, and search filters."""
    return await poc_service.get_pocs_list(
        status_filter=status,
        category_id=category_id,
        search_query=search,
        include_deleted=include_deleted
    )

@router.get("/pocs/{identifier}", response_model=POCResponse)
async def get_poc(identifier: str):
    """Retrieve POC details by unique readable SLUG or UUID."""
    poc = await poc_service.get_poc_by_slug_or_id(identifier)
    if not poc:
        raise HTTPException(status_code=404, detail=f"POC '{identifier}' not found")
    return poc

@router.post("/pocs", response_model=POCResponse, status_code=status.HTTP_201_CREATED)
async def create_poc(payload: POCCreate):
    """Admin CRUD endpoint: Create a new POC with unique slug generation."""
    return await poc_service.create_poc_record(payload.model_dump())

@router.put("/pocs/{poc_id}", response_model=POCResponse)
async def update_poc(poc_id: str, payload: POCUpdate):
    """Admin CRUD endpoint: Update an existing POC."""
    updated = await poc_service.update_poc_record(poc_id, payload.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"POC ID {poc_id} not found")
    return updated

@router.delete("/pocs/{poc_id}")
async def delete_poc(poc_id: str):
    """Admin CRUD endpoint: Soft-delete POC (sets status to DELETED)."""
    success = await poc_service.soft_delete_poc(poc_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"POC ID {poc_id} not found")
    return {"message": f"POC {poc_id} moved to DELETED status successfully"}

@router.post("/pocs/{poc_id}/restore")
async def restore_poc_endpoint(poc_id: str, new_status: str = "PUBLISHED"):
    """Admin CRUD endpoint: Restore a soft-deleted POC."""
    success = await poc_service.restore_poc(poc_id, new_status)
    if not success:
        raise HTTPException(status_code=404, detail=f"POC ID {poc_id} not found")
    return {"message": f"POC {poc_id} restored to status '{new_status}'"}

@router.post("/pocs/{identifier}/view")
async def track_view(identifier: str):
    """Increments telemetry page view count for a POC."""
    views = await poc_service.increment_view_count(identifier)
    return {"views": views}

@router.post("/pocs/{identifier}/demo-request")
async def track_demo_request(identifier: str):
    """Increments telemetry demo request count for a POC."""
    requests = await poc_service.increment_demo_requests(identifier)
    return {"demo_requests": requests}
