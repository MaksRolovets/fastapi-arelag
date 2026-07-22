from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.balance import UserBalance
from schemas.enums import CurrencyEnum
import datetime
from decimal import Decimal

async def get_users_balances(session: AsyncSession,user_ids: list[int]):
    result = await session.execute(select(UserBalance).where(UserBalance.user_id.in_(user_ids)))
    return result.scalars().all()

async def get_balance_user_id(session: AsyncSession, user_id : int, currency : CurrencyEnum | None = None):
    q = select(UserBalance).where(UserBalance.user_id==user_id)
    if currency is not None:
        q = q.where(UserBalance.currency == currency)
    result =  await session.execute(q)
    return result.scalar()

async def create_user_balance(session: AsyncSession,user_id : int):

    balances = [
        UserBalance(
            user_id=user_id,
            currency=currency.value,
            amount=0,
            created=datetime.datetime.utcnow(),
        )
        for currency in CurrencyEnum
    ]

    session.add_all(balances)
    await session.commit()

async def update_user_balance(session: AsyncSession,balance: UserBalance, amount: Decimal) -> UserBalance:
    balance.amount += amount

    await session.flush()
    await session.refresh(balance)

    return balance
        
