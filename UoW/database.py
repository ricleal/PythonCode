"""Database configuration and session management."""

from typing import AsyncGenerator

from models import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# SQLite database URL (using aiosqlite for async support)
DATABASE_URL = "sqlite+aiosqlite:///./access_requests.db"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session."""
    async with AsyncSessionLocal() as session:
        yield session
