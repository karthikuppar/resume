from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Initialize the asynchronous database engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a session factory to manage transactions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for all our models (tables)
Base = declarative_base()

# Dependency to get the database session in our endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()