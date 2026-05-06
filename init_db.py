import asyncio
from app.db.session import engine, Base

async def init_models():
    async with engine.begin() as conn:
        # This creates the tables in your PostgreSQL database
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())