-- Complete Supabase PostgreSQL DDL Schema for Vibodh AI POC Management Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Website Global Settings Table
CREATE TABLE IF NOT EXISTS website_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL DEFAULT 'Vibodh AI Labs',
    tagline VARCHAR(255) DEFAULT 'Think AI. Build Beyond Limits.',
    logo_url TEXT,
    favicon_url TEXT,
    contact_email VARCHAR(255) DEFAULT 'contact@vibodh.ai',
    phone VARCHAR(100),
    address TEXT,
    linkedin_url TEXT DEFAULT 'https://linkedin.com/company/vibodh-ai',
    github_url TEXT DEFAULT 'https://github.com/vibodh-ai',
    instagram_url TEXT,
    youtube_url TEXT,
    footer_text TEXT DEFAULT 'Obsidian Kinetic AI Research & Enterprise Deployment Engine.',
    copyright_text VARCHAR(255) DEFAULT '© Vibodh AI Labs. All rights reserved.',
    google_analytics_id VARCHAR(100),
    google_tag_manager_id VARCHAR(100),
    hero_title TEXT DEFAULT 'Think AI. Build Beyond Limits.',
    hero_subtitle TEXT DEFAULT 'Enterprise-grade autonomous AI solutions, natural language query engines, and high-performance multimodal research.',
    hero_cta_primary_label VARCHAR(100) DEFAULT 'Explore Solutions POCs',
    hero_cta_primary_url VARCHAR(255) DEFAULT '/solutions',
    seo_meta_title VARCHAR(255) DEFAULT 'Vibodh AI Labs - Think AI. Build Beyond.',
    seo_meta_description TEXT DEFAULT 'Enterprise AI Research, Text-to-SQL Translation, and Multimodal Autonomous Agents.',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table (Clerk Auth Integration with RBAC)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY, -- Clerk User ID (e.g. user_2X...)
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'CONTENT_ADMIN', -- SUPER_ADMIN, CONTENT_ADMIN, VIEWER
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Lookup Tables
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    icon VARCHAR(100),
    description TEXT,
    display_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS industries (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    icon VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS technologies (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    logo_url TEXT,
    type VARCHAR(50) DEFAULT 'Framework' -- Language, Framework, Cloud, Database
);

CREATE TABLE IF NOT EXISTS ai_models (
    id VARCHAR(100) PRIMARY KEY,
    provider VARCHAR(100) NOT NULL, -- OpenAI, Anthropic, Custom
    model_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- 4. Main POCs Table (Soft Delete, Telemetry & Advanced SEO)
CREATE TABLE IF NOT EXISTS pocs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_description TEXT NOT NULL,
    full_description TEXT NOT NULL,
    problem_statement TEXT,
    solution_statement TEXT,
    business_benefits TEXT,
    target_users TEXT,
    expected_outcome TEXT,
    category_id VARCHAR(100) REFERENCES categories(id),
    industry_id VARCHAR(100) REFERENCES industries(id),
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT', -- DRAFT, PUBLISHED, ARCHIVED, DELETED
    featured BOOLEAN DEFAULT FALSE,
    featured_order INT DEFAULT 0,
    cover_image TEXT NOT NULL,
    banner_image TEXT,
    architecture_image TEXT,
    demo_video TEXT,
    github_url TEXT,
    live_demo_url TEXT,
    documentation_url TEXT,
    youtube_url TEXT,
    accuracy VARCHAR(50) DEFAULT '99.0%',
    latency VARCHAR(50) DEFAULT '200ms',
    deployment_type VARCHAR(100) DEFAULT 'Cloud Native API',
    project_owner VARCHAR(255),
    contact_email VARCHAR(255),
    
    -- Engagement Telemetry
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    demo_requests INT DEFAULT 0,
    last_viewed_at TIMESTAMP WITH TIME ZONE,

    -- Advanced SEO Metadata
    seo_title VARCHAR(255),
    seo_description TEXT,
    meta_keywords TEXT,
    og_image TEXT,
    twitter_image TEXT,
    canonical_url TEXT,
    sitemap_include BOOLEAN DEFAULT TRUE,
    robots_index BOOLEAN DEFAULT TRUE,

    created_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Relational Sub-Tables with Ordering
CREATE TABLE IF NOT EXISTS features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    feature_name VARCHAR(255) NOT NULL,
    description TEXT,
    display_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    step_order INT DEFAULT 0,
    icon VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS gallery_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    display_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS poc_tags (
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    tag_id VARCHAR(100) REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (poc_id, tag_id)
);

CREATE TABLE IF NOT EXISTS poc_technologies (
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    technology_id VARCHAR(100) REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (poc_id, technology_id)
);

CREATE TABLE IF NOT EXISTS poc_ai_models (
    poc_id UUID REFERENCES pocs(id) ON DELETE CASCADE,
    ai_model_id VARCHAR(100) REFERENCES ai_models(id) ON DELETE CASCADE,
    PRIMARY KEY (poc_id, ai_model_id)
);

-- Indexes for Speed & Search Performance
CREATE INDEX IF NOT EXISTS idx_pocs_slug ON pocs(slug);
CREATE INDEX IF NOT EXISTS idx_pocs_status ON pocs(status);
CREATE INDEX IF NOT EXISTS idx_pocs_category ON pocs(category_id);
CREATE INDEX IF NOT EXISTS idx_pocs_featured ON pocs(featured);

-- 6. Training Materials Module
CREATE TABLE IF NOT EXISTS training_materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT', -- DRAFT, PUBLISHED, ARCHIVED, DELETED
    created_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    training_id UUID REFERENCES training_materials(id) ON DELETE CASCADE,
    resource_name VARCHAR(255) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_url TEXT NOT NULL,
    display_order INT DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_training_slug ON training_materials(slug);
CREATE INDEX IF NOT EXISTS idx_training_status ON training_materials(status);

-- 7. Training Downloads Tracking
CREATE TABLE IF NOT EXISTS training_downloads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    training_id UUID REFERENCES training_materials(id) ON DELETE CASCADE,
    resource_id UUID REFERENCES training_resources(id) ON DELETE CASCADE,
    downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_training_downloads_user ON training_downloads(user_id);
