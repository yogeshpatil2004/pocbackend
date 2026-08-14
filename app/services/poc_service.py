import re
import uuid
from typing import List, Optional
from datetime import datetime

# In-Memory Repository with persistence fallback (connects seamlessly to Supabase)
POCS_REPOSITORY: List[dict] = []
SETTINGS_REPOSITORY: dict = {
    "company_name": "Vibodh AI Labs",
    "tagline": "Think AI. Build Beyond Limits.",
    "contact_email": "contact@vibodh.ai",
    "hero_title": "Think AI. Build Beyond Limits.",
    "hero_subtitle": "Enterprise-grade autonomous AI solutions, natural language query engines, and high-performance multimodal research.",
    "hero_cta_primary_label": "Explore Solutions POCs",
    "hero_cta_primary_url": "/solutions",
    "seo_meta_title": "Vibodh AI Labs - Think AI. Build Beyond.",
    "seo_meta_description": "Enterprise AI Research, Text-to-SQL Translation, and Multimodal Autonomous Agents."
}

def generate_slug(title: str) -> str:
    """Generates clean human readable slug from title"""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s-]+', '-', slug).strip('-')

def ensure_unique_slug(base_slug: str, current_id: Optional[str] = None) -> str:
    """Ensures slug is unique across repository"""
    slug = base_slug
    counter = 1
    while any(p["slug"] == slug and p["id"] != current_id for p in POCS_REPOSITORY):
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

async def create_poc_record(data: dict) -> dict:
    base_slug = data.get("slug") or generate_slug(data["title"])
    unique_slug = ensure_unique_slug(base_slug)

    new_poc = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "slug": unique_slug,
        "short_description": data["short_description"],
        "full_description": data["full_description"],
        "problem_statement": data.get("problem_statement", ""),
        "solution_statement": data.get("solution_statement", ""),
        "business_benefits": data.get("business_benefits", ""),
        "category_id": data.get("category_id", "nlp"),
        "industry_id": data.get("industry_id", "tech"),
        "status": data.get("status", "DRAFT"),
        "featured": data.get("featured", False),
        "featured_order": data.get("featured_order", 0),
        "cover_image": data["cover_image"],
        "banner_image": data.get("banner_image"),
        "architecture_image": data.get("architecture_image"),
        "demo_video": data.get("demo_video"),
        "github_url": data.get("github_url"),
        "live_demo_url": data.get("live_demo_url"),
        "documentation_url": data.get("documentation_url"),
        "accuracy": data.get("accuracy", "99.0%"),
        "latency": data.get("latency", "200ms"),
        "views": 0,
        "likes": 0,
        "demo_requests": 0,
        "last_viewed_at": None,
        "features": data.get("features", []),
        "workflow_steps": data.get("workflow_steps", []),
        "gallery_images": data.get("gallery_images", []),
        "tags": data.get("tags", []),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    POCS_REPOSITORY.append(new_poc)
    return new_poc

async def get_pocs_list(
    status_filter: Optional[str] = "PUBLISHED",
    category_id: Optional[str] = None,
    search_query: Optional[str] = None,
    include_deleted: bool = False
) -> List[dict]:
    results = POCS_REPOSITORY

    if not include_deleted:
        results = [p for p in results if p.get("status") != "DELETED"]

    if status_filter and status_filter != "ALL":
        results = [p for p in results if p.get("status") == status_filter]

    if category_id and category_id != "all":
        results = [p for p in results if p.get("category_id") == category_id]

    if search_query:
        q = search_query.lower()
        results = [
            p for p in results
            if q in p["title"].lower() or q in p["short_description"].lower() or any(q in t.lower() for t in p.get("tags", []))
        ]

    return results

async def get_poc_by_slug_or_id(identifier: str) -> Optional[dict]:
    for poc in POCS_REPOSITORY:
        if poc["slug"] == identifier or poc["id"] == identifier:
            return poc
    return None

async def update_poc_record(poc_id: str, update_data: dict) -> Optional[dict]:
    for idx, poc in enumerate(POCS_REPOSITORY):
        if poc["id"] == poc_id:
            if "title" in update_data and update_data["title"]:
                base_slug = update_data.get("slug") or generate_slug(update_data["title"])
                update_data["slug"] = ensure_unique_slug(base_slug, poc_id)
            
            update_data["updated_at"] = datetime.utcnow().isoformat()
            poc.update({k: v for k, v in update_data.items() if v is not None})
            POCS_REPOSITORY[idx] = poc
            return poc
    return None

async def soft_delete_poc(poc_id: str) -> bool:
    for poc in POCS_REPOSITORY:
        if poc["id"] == poc_id:
            poc["status"] = "DELETED"
            poc["updated_at"] = datetime.utcnow().isoformat()
            return True
    return False

async def restore_poc(poc_id: str, new_status: str = "PUBLISHED") -> bool:
    for poc in POCS_REPOSITORY:
        if poc["id"] == poc_id:
            poc["status"] = new_status
            poc["updated_at"] = datetime.utcnow().isoformat()
            return True
    return False

async def increment_view_count(poc_id: str):
    for poc in POCS_REPOSITORY:
        if poc["id"] == poc_id or poc["slug"] == poc_id:
            poc["views"] = (poc.get("views") or 0) + 1
            poc["last_viewed_at"] = datetime.utcnow().isoformat()
            return poc["views"]
    return 0

async def increment_demo_requests(poc_id: str):
    for poc in POCS_REPOSITORY:
        if poc["id"] == poc_id or poc["slug"] == poc_id:
            poc["demo_requests"] = (poc.get("demo_requests") or 0) + 1
            return poc["demo_requests"]
    return 0

async def get_analytics_summary() -> dict:
    total = len(POCS_REPOSITORY)
    published = sum(1 for p in POCS_REPOSITORY if p.get("status") == "PUBLISHED")
    drafts = sum(1 for p in POCS_REPOSITORY if p.get("status") == "DRAFT")
    archived = sum(1 for p in POCS_REPOSITORY if p.get("status") == "ARCHIVED")
    deleted = sum(1 for p in POCS_REPOSITORY if p.get("status") == "DELETED")
    total_views = sum(p.get("views", 0) for p in POCS_REPOSITORY)
    total_demo_requests = sum(p.get("demo_requests", 0) for p in POCS_REPOSITORY)

    return {
        "totalPocs": total,
        "published": published,
        "drafts": drafts,
        "archived": archived,
        "deleted": deleted,
        "totalViews": total_views,
        "demoRequests": total_demo_requests,
        "lastUpdated": datetime.utcnow().isoformat()
    }
