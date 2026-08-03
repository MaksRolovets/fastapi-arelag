from collections.abc import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


_engine = None
_sessionmaker = None


def get_engine():
    global _engine

    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True,
        )

    return _engine


def get_sessionmaker():
    global _sessionmaker

    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _sessionmaker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_sessionmaker()() as session:
        yield session


async def dispose_engine():
    global _engine
    global _sessionmaker

    if _engine is not None:
        await _engine.dispose()

    _engine = None
    _sessionmaker = None
