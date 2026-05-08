import asyncio
from app.db.session import engine, Base
from app.models.user import User
from app.models.resume import ResumeAnalysisModel # <-- Add this new import

async def init_models():
    async with engine.begin() as conn:
        # This creates the tables in your PostgreSQL database
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())