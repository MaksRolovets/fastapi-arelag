from core.clickhouse import client
from events.schemas import TransactionCreatedEvent


async def insert_transaction_event(event: TransactionCreatedEvent,) -> None:

    client.insert(
        table="transaction_events",
        data=[
            [
                event.transaction_id,
                event.user_id,
                event.amount,
                event.currency,
                event.status,
            ]
        ],
        column_names=[
            "transaction_id",
            "user_id",
            "amount",
            "currency",
            "status",
        ],
    )

async def get_transaction_events():
    result = client.query("""
        SELECT
            transaction_id,
            user_id,
            amount,
            currency,
            status
        FROM analytics.transaction_events
        ORDER BY transaction_id DESC
    """)

    return result.result_rows