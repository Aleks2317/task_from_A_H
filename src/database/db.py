from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import db_user, db_password, db_host, db_port, db_name


DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    future=True
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def create_tables():
    """Creates tables in the database if they do not exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)