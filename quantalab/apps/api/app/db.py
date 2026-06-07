from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

class Base(DeclarativeBase): pass
_settings = get_settings()
engine = create_async_engine(_settings.database_url, echo=_settings.debug, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try: yield session; await session.commit()
        except: await session.rollback(); raise
        finally: await session.close()
