import orjson

from events.schemas import TransactionCreatedEvent


def serialize(event: TransactionCreatedEvent) -> bytes:
    return orjson.dumps(event.model_dump(mode="json"))


def deserialize(data: bytes) -> TransactionCreatedEvent:
    return TransactionCreatedEvent.model_validate(orjson.loads(data))