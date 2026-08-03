import json

from aiokafka import AIOKafkaConsumer

from core.config import settings


async def consume_transactions() -> None:
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_TRANSACTIONS,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="transaction-consumer",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    await consumer.start()

    try:
        async for message in consumer:
            print(
                f"Received message: "
                f"topic={message.topic}, "
                f"partition={message.partition}, "
                f"offset={message.offset}, "
                f"value={message.value}"
            )
    finally:
        await consumer.stop()

