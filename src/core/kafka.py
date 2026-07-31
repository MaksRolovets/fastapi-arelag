import asyncio

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from core.config import settings

producer: AIOKafkaProducer | None = None


async def create_topics() -> None:
    admin = AIOKafkaAdminClient(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    await admin.start()

    try:
        topics = await admin.list_topics()

        if settings.KAFKA_TOPIC_TRANSACTIONS not in topics:
            await admin.create_topics(
                [
                    NewTopic(
                        name=settings.KAFKA_TOPIC_TRANSACTIONS,
                        num_partitions=1,
                        replication_factor=1,
                    )
                ]
            )
    finally:
        await admin.close()


async def start_kafka() -> None:
    global producer

    for _ in range(30):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            )

            await producer.start()
            await create_topics()
            return

        except Exception:
            if producer is not None:
                try:
                    await producer.stop()
                except Exception:
                    pass

            await asyncio.sleep(2)

    raise RuntimeError("Kafka initialization failed.")


async def stop_kafka() -> None:
    global producer

    if producer is not None:
        await producer.stop()