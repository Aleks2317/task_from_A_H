from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session_maker
from src.logging_config import logger


async def get_db_postgres() -> AsyncGenerator[AsyncSession, None]:
    """Dependency generator that provides an async database session.
    Ensures session is closed after use, even if an error occurs."""
    logger.info("Starting a new database session")
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Error during database session: {e}")
            raise
        finally:
            await session.close()
