import asyncio

from celery import shared_task
from celery.result import AsyncResult
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.celery import celery_app
from core.config import settings
from services.analytics import get_transaction_analysis_service

import models

@celery_app.task(name="tasks.generate_transaction_analysis")
def generate_transaction_analysis():
    async def run():
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True,
        )

        sessionmaker = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with sessionmaker() as session:
            result = await get_transaction_analysis_service(session)

        await engine.dispose()

        return [item.model_dump() for item in result]

    return asyncio.run(run())


def get_task_result(task_id: str):
    return AsyncResult(task_id, app=celery_app)