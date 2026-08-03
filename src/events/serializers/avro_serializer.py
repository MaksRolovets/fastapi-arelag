import io
import json
from decimal import Decimal
from pathlib import Path

from fastavro import parse_schema
from fastavro import schemaless_reader
from fastavro import schemaless_writer

from events.schemas import TransactionCreatedEvent


schema_path = Path(__file__).parent.parent / "transaction.avsc"

with open(schema_path, encoding="utf-8") as file:
    schema = parse_schema(json.load(file))


def serialize(event: TransactionCreatedEvent) -> bytes:
    buffer = io.BytesIO()

    schemaless_writer(
        buffer,
        schema,
        {
            "transaction_id": event.transaction_id,
            "user_id": event.user_id,
            "amount": str(event.amount),
            "currency": event.currency,
            "status": event.status,
        },
    )

    return buffer.getvalue()


def deserialize(data: bytes) -> TransactionCreatedEvent:
    buffer = io.BytesIO(data)
    payload = schemaless_reader(buffer,schema)
    payload["amount"] = Decimal(payload["amount"])

    return TransactionCreatedEvent.model_validate(payload)