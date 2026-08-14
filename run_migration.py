import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)

async def run_migration():
    async with engine.begin() as conn:
        with open('schema.sql', 'r') as f:
            sql = f.read()
            
        # Split by ';' to execute commands individually
        commands = [cmd.strip() for cmd in sql.split(';') if cmd.strip()]
        
        for cmd in commands:
            print(f"Executing command...")
            try:
                await conn.execute(text(cmd))
            except Exception as e:
                print(f"Error: {e}")
            
    print("Schema sync complete!")

if __name__ == "__main__":
    asyncio.run(run_migration())
