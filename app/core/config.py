import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibodh AI Labs API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Single Authorized Administrator Email
    ADMIN_EMAIL: str = "vibodh.tv@gmail.com"

    # Supabase PostgreSQL Async URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres_password@db.supabase.co:5432/postgres"
    )

    # Supabase S3 Storage Settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://jogrkimdkssthgcfyyxz.supabase.co")
    SUPABASE_STORAGE_BUCKET: str = os.getenv("SUPABASE_STORAGE_BUCKET", "vibodh_assets")
    SUPABASE_STORAGE_ACCESS_KEY_ID: str = os.getenv("SUPABASE_STORAGE_ACCESS_KEY_ID", "67aac7893847f55c764810f70917108a")
    SUPABASE_STORAGE_SECRET_ACCESS_KEY: str = os.getenv("SUPABASE_STORAGE_SECRET_ACCESS_KEY", "076d888fec122591415cfb6eaa516d5f732e21762fb63d9403b1cdcf53729e21")
    SUPABASE_STORAGE_REGION: str = os.getenv("SUPABASE_STORAGE_REGION", "ap-northeast-1")

    # ImageKit Media Storage Settings
    IMAGEKIT_PUBLIC_KEY: str = os.getenv("IMAGEKIT_PUBLIC_KEY", "public_iGfiHwCipiHE9JKSGEyc857irw4=")
    IMAGEKIT_PRIVATE_KEY: str = os.getenv("IMAGEKIT_PRIVATE_KEY", "private_9nf8NtR0zZAJq9/qpaB3fhPdAgI=")
    IMAGEKIT_URL_ENDPOINT: str = os.getenv("IMAGEKIT_URL_ENDPOINT", "https://ik.imagekit.io/smhak538c")

    # Clerk Auth Settings
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "sk_test_placeholder")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
