import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.session import Base
# Import all models to ensure they are registered with Base
from app.models.training import *

async def run_migrations():
    print("Connecting to DB:", settings.DATABASE_URL)
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(run_migrations())
