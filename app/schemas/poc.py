from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FeatureSchema(BaseModel):
    feature_name: str
    description: Optional[str] = None
    display_order: Optional[int] = 0

class WorkflowStepSchema(BaseModel):
    title: str
    description: Optional[str] = None
    step_order: Optional[int] = 0
    icon: Optional[str] = None

class GalleryImageSchema(BaseModel):
    image_url: str
    display_order: Optional[int] = 0

class TextToSqlRequest(BaseModel):
    query: str

class TextToSqlResponse(BaseModel):
    query: str
    generatedSql: str
    executionTimeMs: int
    tokensUsed: int
    confidenceScore: str
    schemaMatched: str
    results: List[Dict[str, Any]]

class POCBase(BaseModel):
    title: str
    slug: Optional[str] = None
    short_description: str
    full_description: str
    problem_statement: Optional[str] = None
    solution_statement: Optional[str] = None
    business_benefits: Optional[str] = None
    target_users: Optional[str] = None
    expected_outcome: Optional[str] = None
    category_id: Optional[str] = "nlp"
    industry_id: Optional[str] = "tech"
    status: Optional[str] = "DRAFT" # DRAFT, PUBLISHED, ARCHIVED, DELETED
    featured: Optional[bool] = False
    featured_order: Optional[int] = 0
    cover_image: str
    banner_image: Optional[str] = None
    architecture_image: Optional[str] = None
    demo_video: Optional[str] = None
    github_url: Optional[str] = None
    live_demo_url: Optional[str] = None
    documentation_url: Optional[str] = None
    youtube_url: Optional[str] = None
    accuracy: Optional[str] = "99.0%"
    latency: Optional[str] = "200ms"
    deployment_type: Optional[str] = "Cloud Native API"
    project_owner: Optional[str] = "Vibodh Research"
    contact_email: Optional[str] = "contact@vibodh.ai"

    # Advanced SEO
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None
    twitter_image: Optional[str] = None
    canonical_url: Optional[str] = None
    sitemap_include: Optional[bool] = True
    robots_index: Optional[bool] = True

class POCCreate(POCBase):
    features: Optional[List[FeatureSchema]] = []
    workflow_steps: Optional[List[WorkflowStepSchema]] = []
    gallery_images: Optional[List[GalleryImageSchema]] = []
    tags: Optional[List[str]] = []
    technologies: Optional[List[str]] = []
    ai_models: Optional[List[str]] = []

class POCUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    problem_statement: Optional[str] = None
    solution_statement: Optional[str] = None
    business_benefits: Optional[str] = None
    category_id: Optional[str] = None
    industry_id: Optional[str] = None
    status: Optional[str] = None
    featured: Optional[bool] = None
    cover_image: Optional[str] = None
    banner_image: Optional[str] = None
    architecture_image: Optional[str] = None
    demo_video: Optional[str] = None
    github_url: Optional[str] = None
    live_demo_url: Optional[str] = None
    documentation_url: Optional[str] = None
    accuracy: Optional[str] = None
    latency: Optional[str] = None

class POCResponse(POCBase):
    id: str
    slug: str
    views: Optional[int] = 0
    likes: Optional[int] = 0
    demo_requests: Optional[int] = 0
    last_viewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    features: Optional[List[FeatureSchema]] = []
    workflow_steps: Optional[List[WorkflowStepSchema]] = []
    gallery_images: Optional[List[GalleryImageSchema]] = []
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True

class SettingsBase(BaseModel):
    company_name: Optional[str] = "Vibodh AI Labs"
    tagline: Optional[str] = "Think AI. Build Beyond Limits."
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    contact_email: Optional[str] = "contact@vibodh.ai"
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    instagram_url: Optional[str] = None
    youtube_url: Optional[str] = None
    footer_text: Optional[str] = None
    copyright_text: Optional[str] = None
    google_analytics_id: Optional[str] = None
    google_tag_manager_id: Optional[str] = None
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    hero_cta_primary_label: Optional[str] = None
    hero_cta_primary_url: Optional[str] = None
    seo_meta_title: Optional[str] = None
    seo_meta_description: Optional[str] = None

    class Config:
        from_attributes = True
