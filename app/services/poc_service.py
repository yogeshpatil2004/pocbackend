import re
import uuid
from typing import List, Optional
from datetime import datetime

INITIAL_POCS: List[dict] = [
    {
        "id": "1092ccb2-7f06-4ab2-b0c7-9955fad62b5a",
        "title": "Text2SQL Enterprise Engine",
        "slug": "text-to-sql",
        "short_description": "Translate natural language prompts into optimized, production-grade SQL queries with automated schema parsing, RAG query optimization, and execution analytics.",
        "full_description": "Text2SQL Enterprise Engine is an advanced natural language interface for databases. Powered by state-of-the-art Large Language Models (LLMs) and retrieval-augmented generation (RAG), it allows developers, data analysts, and non-technical business users to query complex SQL databases using plain conversational language.",
        "problem_statement": "Writing complex SQL queries across dozens of relational database schemas requires specialized data engineering knowledge and delays time-to-insight for non-technical stakeholders.",
        "solution_statement": "Text2SQL converts natural language questions directly into syntactically valid, schema-aware SQL queries with sub-second execution speeds, automated error correction, and execution safety checks.",
        "business_benefits": "Accelerates business intelligence reporting by 10x, reduces database engineer query assistance requests by 80%, and enables conversational self-service analytics for enterprise teams.",
        "target_users": "Data Analysts, Product Managers, Enterprise Business Intelligence Teams",
        "expected_outcome": "Sub-second SQL generation with 99.4% syntax accuracy across PostgreSQL and Supabase schemas.",
        "category_id": "nlp",
        "industry_id": "enterprise",
        "status": "PUBLISHED",
        "featured": True,
        "featured_order": 1,
        "cover_image": "https://ik.imagekit.io/smhak538c/vibodh_poc/text2sql_cover_N1uI4gQk9.png",
        "banner_image": "https://ik.imagekit.io/smhak538c/vibodh_poc/text2sql_banner_WfS5_G6L3.png",
        "live_demo_url": "https://txt2sql.vibodh.workers.dev/",
        "github_url": None,
        "tags": ["Text-to-SQL", "LLM", "PostgreSQL", "Supabase", "FastAPI", "Cloudflare Workers"],
        "views": 142,
        "likes": 28,
        "demo_requests": 14,
        "features": [
            {"feature_name": "Automated Schema Extraction", "description": "Connects to PostgreSQL/Supabase databases and automatically parses tables, foreign keys, and indexes."},
            {"feature_name": "RAG Query Optimization", "description": "Retrieves relevant table contexts using semantic search before constructing prompt payloads."},
            {"feature_name": "SQL Safety & Sanity Checker", "description": "Ensures generated queries are read-only SELECT statements, preventing destructive DDL/DML execution."}
        ],
        "workflow_steps": [
            {"title": "Natural Language Input", "description": "User enters a question in plain English (e.g., 'Show total sales by product category for Q3')."},
            {"title": "Schema Context Retrieval", "description": "RAG engine fetches table DDLs and column definitions matching the query intent."},
            {"title": "LLM SQL Generation", "description": "Language model generates optimized SQL query with syntax validation."},
            {"title": "Database Execution & Results", "description": "Query executes against live database and displays visual data tables."}
        ],
        "gallery_images": [],
        "created_at": "2026-08-14T10:00:00.000000",
        "updated_at": "2026-08-14T10:00:00.000000"
    },
    {
        "id": "1092ccb2-7f06-4ab2-b0c7-9955fad62b5c",
        "title": "Naidile Naturals - Ayurvedic Commerce Platform",
        "slug": "naidile-naturals",
        "short_description": "Whole-plant, toxin-free Ayurvedic skin and hair care ecommerce platform powered by automated product recommendation engines and custom formulation trial packs.",
        "full_description": "Naidile Naturals is a next-generation Ayurvedic wellness and personal care ecommerce platform. Built to deliver whole-plant, toxin-free skin and hair care formulations crafted from pure botanicals and herbal extracts. The platform features an intelligent recommendation workflow for custom skin-type analysis, interactive trial combo builder, real-time order processing, and holistic product care subscriptions.",
        "problem_statement": "Traditional skincare products often contain synthetic toxins, while consumers struggle to identify genuine, whole-plant Ayurvedic treatments suited for their specific skin type, pigmentation, or pimple care needs.",
        "solution_statement": "Naidile Naturals provides a digital-first Ayurvedic commerce experience with personalized product recommendations, ingredient transparency, automated combo trial packs, and seamless omnichannel delivery.",
        "business_benefits": "Increases customer conversion by 45% with tailored herbal trial packs, builds long-term brand trust with 100% toxin-free guarantee, and streamlines catalog management across 50+ botanical formulations.",
        "target_users": "Consumers, Dermatology Enthusiasts, Wellness Shoppers",
        "expected_outcome": "Seamless Ayurvedic skincare discovery with 99.8% customer satisfaction and instant cart checkout.",
        "category_id": "ecommerce",
        "industry_id": "wellness",
        "status": "PUBLISHED",
        "featured": True,
        "featured_order": 2,
        "cover_image": "https://ik.imagekit.io/smhak538c/vibodh_poc/naidile_ayurveda_cover_hEdhlSlw6.png",
        "banner_image": "https://ik.imagekit.io/smhak538c/vibodh_poc/naidile_ayurveda_cover_hEdhlSlw6.png",
        "live_demo_url": "https://naidile.in",
        "github_url": None,
        "tags": ["Ayurveda", "Ecommerce", "Skin Care", "SvelteKit", "Botanical Formulations", "Toxin-Free"],
        "views": 98,
        "likes": 19,
        "demo_requests": 8,
        "features": [
            {"feature_name": "Intelligent Product Personalization", "description": "AI-guided recommendation engine matching skin concerns with pure botanical formulations."},
            {"feature_name": "Toxin-Free Botanical Catalog", "description": "Multi-category herbal skincare showcase featuring Kumkumadi Creams, De-Pigmentation formulations, and natural cleansers."},
            {"feature_name": "Custom Combo Trial Builder", "description": "Interactive trial pack configurator allowing customers to mix & match 4-in-1 trial sizes."}
        ],
        "workflow_steps": [
            {"title": "Skin Assessment & Discovery", "description": "Customer takes a quick 3-step skin questionnaire or explores targeted remedies."},
            {"title": "Formulation Matching", "description": "Engine matches symptoms (pigmentation, acne, hydration) with whole-plant herbal remedies."},
            {"title": "Custom Trial Pack Assembly", "description": "Customer selects or receives an auto-generated trial combo pack."}
        ],
        "gallery_images": [],
        "created_at": "2026-08-14T10:25:00.000000",
        "updated_at": "2026-08-14T10:25:00.000000"
    }
]

POCS_REPOSITORY: List[dict] = list(INITIAL_POCS)
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

async def get_categories_list() -> List[dict]:
    return [
        {"id": "all", "name": "All Solutions"},
        {"id": "nlp", "name": "NLP & Text-to-SQL"},
        {"id": "ecommerce", "name": "Ayurveda & Ecommerce"},
        {"id": "vision", "name": "Computer Vision"},
        {"id": "audio", "name": "Voice & Speech AI"},
        {"id": "agents", "name": "Autonomous Agents"}
    ]
