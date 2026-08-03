from decimal import Decimal

from fastapi import APIRouter

from events.producer import publish_transaction_created
from events.schemas import TransactionCreatedEvent

router = APIRouter(
    prefix="/kafka",
    tags=["Kafka"],
)


@router.post("/test")
async def send_test_message():
    event = TransactionCreatedEvent(
        transaction_id=1,
        user_id=1,
        amount=Decimal("100.50"),
        currency="USD",
        status="SUCCESS",
    )

    await publish_transaction_created(event)

    return {"message": "Message sent successfully."}