from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session_maker


async def get_db_postgres() -> AsyncGenerator[AsyncSession, None]:
    """Dependency generator that provides an async database session.
    Ensures session is closed after use, even if an error occurs."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
