import asyncio
from core.clickhouse import create_tables

from events.consumer import consume_transactions

if __name__ == "__main__":
    create_tables()     
    asyncio.run(consume_transactions())