import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, desc
from app.models.training import (
    TrainingMaterial, TrainingResource, TrainingDownload
)
from app.schemas.training import TrainingMaterialCreate, TrainingMaterialUpdate
import re

def generate_slug(title: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s-]+', '-', slug).strip('-')

async def ensure_unique_slug(db: AsyncSession, base_slug: str, current_id: Optional[str] = None) -> str:
    slug = base_slug
    counter = 1
    while True:
        query = select(TrainingMaterial).filter(TrainingMaterial.slug == slug)
        if current_id:
            query = query.filter(TrainingMaterial.id != current_id)
        result = await db.execute(query)
        if not result.scalars().first():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

async def create_training(db: AsyncSession, data: TrainingMaterialCreate) -> TrainingMaterial:
    base_slug = data.slug or generate_slug(data.title)
    unique_slug = await ensure_unique_slug(db, base_slug)

    new_training = TrainingMaterial(
        title=data.title,
        slug=unique_slug,
        short_description=data.short_description,
        status=data.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(new_training)
    await db.flush()

    for res in data.resources:
        res_dict = res.model_dump()
        res_dict["training_id"] = new_training.id
        r = TrainingResource(**res_dict)
        db.add(r)

    await db.commit()
    await db.refresh(new_training)
    return await get_training_by_id_or_slug(db, new_training.id)

async def get_trainings(
    db: AsyncSession,
    status_filter: Optional[str] = "PUBLISHED",
    search: Optional[str] = None,
    include_deleted: bool = False
) -> List[TrainingMaterial]:
    query = select(TrainingMaterial).options(
        selectinload(TrainingMaterial.resources)
    )

    if not include_deleted:
        query = query.filter(TrainingMaterial.status != "DELETED")
    if status_filter and status_filter != "ALL":
        query = query.filter(TrainingMaterial.status == status_filter)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                TrainingMaterial.title.ilike(search_pattern),
                TrainingMaterial.short_description.ilike(search_pattern)
            )
        )
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_training_by_id_or_slug(db: AsyncSession, identifier: str) -> Optional[TrainingMaterial]:
    query = select(TrainingMaterial).options(
        selectinload(TrainingMaterial.resources)
    )
    
    try:
        uuid_val = uuid.UUID(str(identifier))
        query = query.filter(
            or_(
                TrainingMaterial.id == uuid_val,
                TrainingMaterial.slug == str(identifier)
            )
        )
    except ValueError:
        query = query.filter(TrainingMaterial.slug == str(identifier))

    result = await db.execute(query)
    return result.scalars().first()

async def update_training(db: AsyncSession, training_id: str, data: TrainingMaterialUpdate) -> Optional[TrainingMaterial]:
    try:
        uuid_val = uuid.UUID(str(training_id))
    except ValueError:
        return None

    query = select(TrainingMaterial).options(selectinload(TrainingMaterial.resources)).filter(TrainingMaterial.id == uuid_val)
    result = await db.execute(query)
    training = result.scalars().first()
    if not training:
        return None

    update_data = data.model_dump(exclude_unset=True)
    
    if "title" in update_data and update_data["title"]:
        base_slug = update_data.get("slug") or generate_slug(update_data["title"])
        update_data["slug"] = await ensure_unique_slug(db, base_slug, training.id)

    for key, value in update_data.items():
        if key not in ["resources"]:
            setattr(training, key, value)
            
    training.updated_at = datetime.utcnow()
            
    if "resources" in update_data:
        await db.execute(TrainingResource.__table__.delete().where(TrainingResource.training_id == training.id))
        for res in update_data["resources"]:
            res_dict = res if isinstance(res, dict) else res.model_dump()
            res_dict["training_id"] = training.id
            db.add(TrainingResource(**res_dict))
    
    await db.commit()
    return await get_training_by_id_or_slug(db, str(training.id))

async def delete_training(db: AsyncSession, training_id: str) -> bool:
    try:
        uuid_val = uuid.UUID(str(training_id))
    except ValueError:
        return False

    query = select(TrainingMaterial).filter(TrainingMaterial.id == uuid_val)
    result = await db.execute(query)
    training = result.scalars().first()
    if not training:
        return False
    training.status = "DELETED"
    training.updated_at = datetime.utcnow()
    await db.commit()
    return True

async def record_download(db: AsyncSession, user_id: str, training_id: str, resource_id: str) -> TrainingDownload:
    download = TrainingDownload(
        user_id=user_id,
        training_id=uuid.UUID(str(training_id)),
        resource_id=uuid.UUID(str(resource_id)),
        downloaded_at=datetime.utcnow()
    )
    db.add(download)
    await db.commit()
    await db.refresh(download)
    return download

async def get_user_downloads(db: AsyncSession, user_id: str) -> List[TrainingDownload]:
    query = (
        select(TrainingDownload)
        .options(
            selectinload(TrainingDownload.training),
            selectinload(TrainingDownload.resource)
        )
        .filter(TrainingDownload.user_id == user_id)
        .order_by(desc(TrainingDownload.downloaded_at))
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_folder_contents(db: AsyncSession, folder_id: Optional[str] = None) -> dict:
    breadcrumbs = [{"id": None, "name": "Training Materials"}]
    current_folder = None
    
    if folder_id:
        try:
            f_uuid = uuid.UUID(str(folder_id))
            curr_res = await db.execute(select(TrainingFolder).filter(TrainingFolder.id == f_uuid))
            current_folder = curr_res.scalars().first()
        except ValueError:
            current_folder = None
            
    if current_folder:
        # Build breadcrumbs chain recursively
        chain = []
        curr = current_folder
        while curr:
            chain.append({"id": str(curr.id), "name": curr.name})
            if curr.parent_id:
                p_res = await db.execute(select(TrainingFolder).filter(TrainingFolder.id == curr.parent_id))
                curr = p_res.scalars().first()
            else:
                curr = None
        chain.reverse()
        breadcrumbs.extend(chain)

        # Get subfolders
        sub_res = await db.execute(
            select(TrainingFolder)
            .filter(TrainingFolder.parent_id == current_folder.id)
            .order_by(TrainingFolder.name)
        )
        folders = sub_res.scalars().all()

        # Get resources inside current folder
        rec_res = await db.execute(
            select(TrainingResource)
            .filter(TrainingResource.folder_id == current_folder.id)
            .order_by(TrainingResource.resource_name)
        )
        resources = rec_res.scalars().all()
    else:
        # Root level
        sub_res = await db.execute(
            select(TrainingFolder)
            .filter(TrainingFolder.parent_id.is_(None))
            .order_by(TrainingFolder.name)
        )
        folders = sub_res.scalars().all()

        rec_res = await db.execute(
            select(TrainingResource)
            .filter(TrainingResource.folder_id.is_(None))
            .order_by(TrainingResource.resource_name)
        )
        resources = rec_res.scalars().all()

    return {
        "current_folder": current_folder,
        "breadcrumbs": breadcrumbs,
        "folders": folders,
        "resources": resources
    }

async def create_folder(db: AsyncSession, name: str, parent_id: Optional[str] = None) -> TrainingFolder:
    p_uuid = uuid.UUID(str(parent_id)) if parent_id and parent_id != 'null' else None
    new_folder = TrainingFolder(name=name.strip(), parent_id=p_uuid)
    db.add(new_folder)
    await db.commit()
    await db.refresh(new_folder)
    return new_folder

async def delete_folder(db: AsyncSession, folder_id: str) -> bool:
    try:
        f_uuid = uuid.UUID(str(folder_id))
        folder = await db.get(TrainingFolder, f_uuid)
        if not folder:
            return False
        await db.delete(folder)
        await db.commit()
        return True
    except Exception:
        return False

async def create_standalone_resource(db: AsyncSession, data: dict) -> TrainingResource:
    f_uuid = uuid.UUID(str(data["folder_id"])) if data.get("folder_id") and data.get("folder_id") != 'null' else None
    t_uuid = uuid.UUID(str(data["training_id"])) if data.get("training_id") and data.get("training_id") != 'null' else None
    new_res = TrainingResource(
        resource_name=data["resource_name"].strip(),
        resource_type=data["resource_type"],
        resource_url=data["resource_url"].strip(),
        folder_id=f_uuid,
        training_id=t_uuid
    )
    db.add(new_res)
    await db.commit()
    await db.refresh(new_res)
    return new_res

async def delete_standalone_resource(db: AsyncSession, resource_id: str) -> bool:
    try:
        r_uuid = uuid.UUID(str(resource_id))
        res = await db.get(TrainingResource, r_uuid)
        if not res:
            return False
        await db.delete(res)
        await db.commit()
        return True
    except Exception:
        return False

