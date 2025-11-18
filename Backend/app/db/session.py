from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
from sqlalchemy import create_engine

engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
