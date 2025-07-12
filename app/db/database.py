# air_quality_app/app/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Construct the async database URL from settings
ASYNC_DATABASE_URL = settings.DATABASE_URL

# Create the asynchronous engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True) # echo=True for SQL logging (useful in dev)

# Create an asynchronous sessionmaker
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession, # Specify AsyncSession for async context
    expire_on_commit=False # Important for async usage: objects don't detach immediately
)

# Base class for your SQLAlchemy models
Base = declarative_base()

# Dependency to get an async database session for API endpoints
async def get_db_session():
    """Dependency that provides an AsyncSession for database operations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() # Ensure session is closed