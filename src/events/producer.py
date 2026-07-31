import orjson

import core.kafka as kafka
from core.config import settings
from events.schemas import TransactionCreatedEvent


async def publish_transaction_created(
    event: TransactionCreatedEvent,
) -> None:
    if kafka.producer is None:
        raise RuntimeError("Kafka producer is not initialized.")

    await kafka.producer.send_and_wait(
        topic=settings.KAFKA_TOPIC_TRANSACTIONS,
        value=orjson.dumps(event.model_dump(mode="json")),
    )