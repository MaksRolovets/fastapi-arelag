import asyncio

from events.consumer import consume_transactions

print("=== CONSUMER ENTRYPOINT STARTED ===")

if __name__ == "__main__":
    asyncio.run(consume_transactions())