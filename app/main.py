# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "traceback": traceback.format_exc()}
    )

# Enable CORS for frontend Vite dev server & production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def on_startup():
    from sqlalchemy import text
    from app.db.session import engine
    from app.db.session import Base
    from app.models.training import TrainingFolder, TrainingResource, TrainingMaterial, TrainingDownload  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.connect() as conn:
        for sql in [
            "ALTER TABLE training_resources ADD COLUMN IF NOT EXISTS folder_name VARCHAR DEFAULT 'General Resources';",
            "ALTER TABLE training_resources ADD COLUMN IF NOT EXISTS folder_id UUID;",
            "ALTER TABLE training_resources ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();"
        ]:
            try:
                await conn.execute(text(sql))
                await conn.commit()
            except Exception as e:
                print("Auto schema sync notice:", e)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs": "/docs",
        "version": settings.VERSION
    }
