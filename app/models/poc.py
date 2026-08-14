from sqlalchemy import Column, String, Text, Boolean, Integer, JSON, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# Association Tables
poc_tags_table = Table(
    'poc_tags',
    Base.metadata,
    Column('poc_id', String, ForeignKey('pocs.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

poc_technologies_table = Table(
    'poc_technologies',
    Base.metadata,
    Column('poc_id', String, ForeignKey('pocs.id', ondelete='CASCADE'), primary_key=True),
    Column('technology_id', String, ForeignKey('technologies.id', ondelete='CASCADE'), primary_key=True)
)

poc_ai_models_table = Table(
    'poc_ai_models',
    Base.metadata,
    Column('poc_id', String, ForeignKey('pocs.id', ondelete='CASCADE'), primary_key=True),
    Column('ai_model_id', String, ForeignKey('ai_models.id', ondelete='CASCADE'), primary_key=True)
)

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String)
    description = Column(Text)
    display_order = Column(Integer, default=0)

class Industry(Base):
    __tablename__ = "industries"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String)

class Technology(Base):
    __tablename__ = "technologies"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    logo_url = Column(Text)
    type = Column(String, default="Framework")

class AIModel(Base):
    __tablename__ = "ai_models"
    id = Column(String, primary_key=True)
    provider = Column(String, nullable=False)
    model_name = Column(String, nullable=False)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Feature(Base):
    __tablename__ = "features"
    id = Column(String, primary_key=True, default=generate_uuid)
    poc_id = Column(String, ForeignKey("pocs.id", ondelete="CASCADE"))
    feature_name = Column(String, nullable=False)
    description = Column(Text)
    display_order = Column(Integer, default=0)

class WorkflowStep(Base):
    __tablename__ = "workflow_steps"
    id = Column(String, primary_key=True, default=generate_uuid)
    poc_id = Column(String, ForeignKey("pocs.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(Text)
    step_order = Column(Integer, default=0)
    icon = Column(String)

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    id = Column(String, primary_key=True, default=generate_uuid)
    poc_id = Column(String, ForeignKey("pocs.id", ondelete="CASCADE"))
    image_url = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)

class WebsiteSettings(Base):
    __tablename__ = "website_settings"
    id = Column(String, primary_key=True, default=generate_uuid)
    company_name = Column(String, default="Vibodh AI Labs")
    tagline = Column(String, default="Think AI. Build Beyond Limits.")
    logo_url = Column(Text)
    favicon_url = Column(Text)
    contact_email = Column(String, default="contact@vibodh.ai")
    phone = Column(String)
    address = Column(Text)
    linkedin_url = Column(Text)
    github_url = Column(Text)
    instagram_url = Column(Text)
    youtube_url = Column(Text)
    footer_text = Column(Text)
    copyright_text = Column(String)
    google_analytics_id = Column(String)
    google_tag_manager_id = Column(String)
    hero_title = Column(Text)
    hero_subtitle = Column(Text)
    hero_cta_primary_label = Column(String)
    hero_cta_primary_url = Column(String)
    seo_meta_title = Column(String)
    seo_meta_description = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class POC(Base):
    __tablename__ = "pocs"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    short_description = Column(Text, nullable=False)
    full_description = Column(Text, nullable=False)
    problem_statement = Column(Text)
    solution_statement = Column(Text)
    business_benefits = Column(Text)
    target_users = Column(Text)
    expected_outcome = Column(Text)
    category_id = Column(String, ForeignKey("categories.id"))
    industry_id = Column(String, ForeignKey("industries.id"))
    status = Column(String, default="DRAFT") # DRAFT, PUBLISHED, ARCHIVED, DELETED
    featured = Column(Boolean, default=False)
    featured_order = Column(Integer, default=0)
    cover_image = Column(Text, nullable=False)
    banner_image = Column(Text)
    architecture_image = Column(Text)
    demo_video = Column(Text)
    github_url = Column(Text)
    live_demo_url = Column(Text)
    documentation_url = Column(Text)
    youtube_url = Column(Text)
    accuracy = Column(String, default="99.0%")
    latency = Column(String, default="200ms")
    deployment_type = Column(String, default="Cloud Native API")
    project_owner = Column(String)
    contact_email = Column(String)

    # Engagement Telemetry
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    demo_requests = Column(Integer, default=0)
    last_viewed_at = Column(DateTime(timezone=True))

    # SEO Metadata
    seo_title = Column(String)
    seo_description = Column(Text)
    meta_keywords = Column(Text)
    og_image = Column(Text)
    twitter_image = Column(Text)
    canonical_url = Column(Text)
    sitemap_include = Column(Boolean, default=True)
    robots_index = Column(Boolean, default=True)

    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category")
    industry = relationship("Industry")
    features = relationship("Feature", cascade="all, delete-orphan")
    workflow_steps = relationship("WorkflowStep", cascade="all, delete-orphan")
    gallery_images = relationship("GalleryImage", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=poc_tags_table)
    technologies = relationship("Technology", secondary=poc_technologies_table)
    ai_models = relationship("AIModel", secondary=poc_ai_models_table)
