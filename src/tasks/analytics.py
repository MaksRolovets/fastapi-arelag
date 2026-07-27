from core.broker import broker
import models
from db.database import get_sessionmaker
from services.analytics import get_transaction_analysis_service


@broker.task
async def generate_transaction_analysis():
    sessionmaker = get_sessionmaker()

    async with sessionmaker() as session:
        return await get_transaction_analysis_service(session)

