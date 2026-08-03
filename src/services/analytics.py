from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from events.schemas import TransactionCreatedEvent
from repositories.clickhouse import insert_transaction_event
from repositories.clickhouse import get_transaction_events
from schemas.analytics import TransactionAnalyticsModel

from repositories.analytics import (
    get_registered_users_count,
    get_registered_and_deposit_users_count,
    get_registered_and_not_rollbacked_deposit_users_count,
    get_not_rollbacked_deposit_amount,
    get_not_rollbacked_withdraw_amount,
    get_transactions_count,
    get_not_rollbacked_transactions_count,
)

from schemas.analytics import TransactionAnalysisModel


async def get_transaction_analysis_service(
    session: AsyncSession,
) -> list[TransactionAnalysisModel]:

    dt_gt = datetime.utcnow().date() - timedelta(weeks=1) + timedelta(days=1)
    dt_lt = datetime.utcnow().date()

    results: list[TransactionAnalysisModel] = []

    for _ in range(52):

        registered_users_count = await get_registered_users_count(
            session=session,
            dt_gt=dt_gt,
            dt_lt=dt_lt,
        )

        registered_and_deposit_users_count = (
            await get_registered_and_deposit_users_count(
                session=session,
                dt_gt=dt_gt,
                dt_lt=dt_lt,
            )
        )

        registered_and_not_rollbacked_deposit_users_count = (
            await get_registered_and_not_rollbacked_deposit_users_count(
                session=session,
                dt_gt=dt_gt,
                dt_lt=dt_lt,
            )
        )

        not_rollbacked_deposit_amount = (
            await get_not_rollbacked_deposit_amount(
                session=session,
                dt_gt=dt_gt,
                dt_lt=dt_lt,
            )
        )

        not_rollbacked_withdraw_amount = (
            await get_not_rollbacked_withdraw_amount(
                session=session,
                dt_gt=dt_gt,
                dt_lt=dt_lt,
            )
        )

        transactions_count = await get_transactions_count(
            session=session,
            dt_gt=dt_gt,
            dt_lt=dt_lt,
        )

        not_rollbacked_transactions_count = (
            await get_not_rollbacked_transactions_count(
                session=session,
                dt_gt=dt_gt,
                dt_lt=dt_lt,
            )
        )

        result = TransactionAnalysisModel(
            start_date=dt_gt,
            end_date=dt_lt,
            registered_users_count=registered_users_count,
            registered_and_deposit_users_count=registered_and_deposit_users_count,
            registered_and_not_rollbacked_deposit_users_count=registered_and_not_rollbacked_deposit_users_count,
            not_rollbacked_deposit_amount=not_rollbacked_deposit_amount,
            not_rollbacked_withdraw_amount=not_rollbacked_withdraw_amount,
            transactions_count=transactions_count,
            not_rollbacked_transactions_count=not_rollbacked_transactions_count,
        )

        if any(
            (
                result.registered_users_count,
                result.registered_and_deposit_users_count,
                result.registered_and_not_rollbacked_deposit_users_count,
                result.not_rollbacked_deposit_amount,
                result.not_rollbacked_withdraw_amount,
                result.transactions_count,
                result.not_rollbacked_transactions_count,
            )
        ):
            results.append(result)

        dt_gt -= timedelta(weeks=1)
        dt_lt -= timedelta(weeks=1)

    return results


async def process_transaction_created_event(
    event: TransactionCreatedEvent,
) -> None:
    await insert_transaction_event(event)



async def get_transaction_events_service():
    rows = await get_transaction_events()

    return [
        TransactionAnalyticsModel(
            transaction_id=row[0],
            user_id=row[1],
            amount=row[2],
            currency=row[3],
            status=row[4],
        )
        for row in rows
    ]