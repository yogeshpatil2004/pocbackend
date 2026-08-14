import asyncio
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.schemas.training import TrainingMaterialCreate
from app.services.training_service import create_training

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def test_create():
    async with async_session() as db:
        data = TrainingMaterialCreate(
            title="Test Training",
            short_description="desc",
            status="PUBLISHED",
            resources=[]
        )
        try:
            res = await create_training(db, data)
            print("Success:", res.id)
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_create())
