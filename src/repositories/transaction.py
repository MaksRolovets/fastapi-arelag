from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from models.transaction import Transaction
from schemas.transaction import TransactionStatusEnum, TransactionModel
from schemas.enums import CurrencyEnum


import datetime

async def get_all_transactions(session : AsyncSession, user_id : int | None = None):
    q = select(Transaction).where(Transaction.is_active != False)
    if user_id:
        q = q.where(Transaction.user_id == user_id)
    transactions = await session.execute(q)
    return transactions.scalars()

async def get_transactions_by_id(session : AsyncSession, trans_id : int):
    result = await session.execute(select(Transaction).where(Transaction.id == trans_id))
    return result.scalar()

async def create_transaction(session: AsyncSession,user_id: int,currency: CurrencyEnum,amount: Decimal,) -> Transaction:
    transaction = Transaction(
                    user_id=user_id,
                    currency=currency.value,
                    amount=amount,
                    status=TransactionStatusEnum.processed.value)

    session.add(transaction)

    await session.flush()
    await session.refresh(transaction)

    return transaction

async def update_transaction(session: AsyncSession, transaction : Transaction, currency: CurrencyEnum):
    transaction.status = currency.value
    await session.flush()
    await session.refresh(transaction)
    return transaction
    