import clickhouse_connect

from core.config import settings

client = clickhouse_connect.get_client(
    host=settings.CLICKHOUSE_HOST,
    port=settings.CLICKHOUSE_PORT,
    username=settings.CLICKHOUSE_USER,
    password=settings.CLICKHOUSE_PASSWORD,
    database=settings.CLICKHOUSE_DATABASE,
)
print(client.ping())

def create_tables() -> None:
    client.command("""
        CREATE TABLE IF NOT EXISTS transaction_events
        (
            transaction_id UInt64,
            user_id UInt64,
            amount Decimal(18,2),
            currency String,
            status String,
            received_at DateTime DEFAULT now()
        )
        ENGINE = MergeTree
        ORDER BY (received_at, transaction_id)
    """)