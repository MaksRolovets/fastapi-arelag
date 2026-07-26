import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from main import app
from db.database import (
    get_async_session,
    get_sessionmaker,
    dispose_engine,
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    Session = get_sessionmaker()

    async with Session() as session:

        await session.execute(text('DELETE FROM "transaction";'))
        await session.execute(text("DELETE FROM user_balance;"))
        await session.execute(text('DELETE FROM "user";'))
        await session.commit()

        yield session

        await session.execute(text('DELETE FROM "transaction";'))
        await session.execute(text("DELETE FROM user_balance;"))
        await session.execute(text('DELETE FROM "user";'))
        await session.commit()

    await dispose_engine()


async def override_get_session():
    Session = get_sessionmaker()

    async with Session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_session):

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
#запуск тестов docker compose exec app python -m pytest tests -v