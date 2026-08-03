import typing
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from schemas.enums import  CurrencyEnum, TransactionStatusEnum

class RequestTransactionModel(BaseModel):
    currency: CurrencyEnum
    amount: Decimal

class TransactionModel(BaseModel):
    id: typing.Optional[int]
    user_id: typing.Optional[int] = None
    currency: typing.Optional[CurrencyEnum] = None
    amount: typing.Optional[float] = None
    status: typing.Optional[TransactionStatusEnum] = None
    created: typing.Optional[datetime] = None
