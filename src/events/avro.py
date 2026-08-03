import io
import json

from fastavro import parse_schema
from fastavro import schemaless_reader
from fastavro import schemaless_writer


with open("events/transaction.avsc") as f:
    schema = parse_schema(json.load(f))


def serialize(data: dict) -> bytes:
    buffer = io.BytesIO()
    schemaless_writer(buffer,schema,data)

    return buffer.getvalue()


def deserialize(data: bytes) -> dict:
    buffer = io.BytesIO(data)

    return schemaless_reader(buffer,schema)