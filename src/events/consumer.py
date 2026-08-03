import json

from aiokafka import AIOKafkaConsumer
from services.analytics import process_transaction_created_event
from core.config import settings
from events.serializers import deserialize

async def consume_transactions() -> None:
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_TRANSACTIONS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="transaction-consumer",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()

    try:
        async for message in consumer:
            event = deserialize(message.value)
            await process_transaction_created_event(event)
    finally:
        await consumer.stop()

