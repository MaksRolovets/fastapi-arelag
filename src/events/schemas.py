from decimal import Decimal

from pydantic import BaseModel


class TransactionCreatedEvent(BaseModel):
    transaction_id: int
    user_id: int
    amount: Decimal
    currency: str
    status: str