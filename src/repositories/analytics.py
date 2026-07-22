from datetime import  date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from models.user import User
from models.transaction import Transaction
from schemas.enums import CurrencyEnum

EXCHANGE_RATES_TO_USD = {
    CurrencyEnum.USD: 1,
    CurrencyEnum.EUR: 0.9342,
    CurrencyEnum.AUD: 0.5447,
    CurrencyEnum.CAD: 0.6162,
    CurrencyEnum.ARS: 0.0009,
    CurrencyEnum.PLN: 0.2343,
    CurrencyEnum.BTC: 100000.0,
    CurrencyEnum.ETH: 3557.3476,
    CurrencyEnum.DOGE: 0.3627,
    CurrencyEnum.USDT: 0.9709,
}

async def get_registered_users_count(session: AsyncSession, dt_gt: date, dt_lt: date)-> int:
    q = select(func.count(User.id)).where((func.date(User.created) >= dt_gt), (func.date(User.created) <= dt_lt), User.is_active != False)
    result = await session.execute(q)
    return result.scalar_one()


async def get_registered_and_deposit_users_count(session: AsyncSession, dt_gt: date, dt_lt: date):
    users_result = await session.execute(
    select(User.id).where(
        func.date(User.created) >= dt_gt,
        func.date(User.created) <= dt_lt,
        User.is_active != False,
    )
)

    user_ids = users_result.scalars().all()

    if not user_ids:
        return 0

    transactions_result = await session.execute(
        select(Transaction.user_id).where(
            func.date(Transaction.created) >= dt_gt,
            func.date(Transaction.created) <= dt_lt,
            Transaction.amount > 0,
            Transaction.user_id.in_(user_ids),
            Transaction.is_active != False,
        )
    )

    transaction_user_ids = set(transactions_result.scalars().all())
    return len(transaction_user_ids)


async def get_registered_and_not_rollbacked_deposit_users_count(session: AsyncSession, dt_gt: date, dt_lt: date):
    users_result = await session.execute(
        select(User.id).where(
            func.date(User.created) >= dt_gt,
            func.date(User.created) <= dt_lt,
            User.is_active != False,
        )
    )

    user_ids = users_result.scalars().all()

    if not user_ids:
        return 0

    transactions_result = await session.execute(
        select(Transaction.user_id).where(
            func.date(Transaction.created) >= dt_gt,
            func.date(Transaction.created) <= dt_lt,
            Transaction.amount > 0,
            Transaction.status != "ROLLBACKED",
            Transaction.user_id.in_(user_ids),
            Transaction.is_active != False,
        )
    )

    transaction_user_ids = set(transactions_result.scalars().all())
    return len(transaction_user_ids)


async def get_not_rollbacked_deposit_amount(session: AsyncSession, dt_gt: date, dt_lt: date):
    q = (
        select(Transaction)
        .where(
            func.date(Transaction.created) >= dt_gt,
            func.date(Transaction.created) <= dt_lt,
            Transaction.amount > 0,
            Transaction.status != "ROLLBACKED",
            Transaction.is_active != False,
        )
    )

    result = await session.execute(q)
    transactions = result.scalars().all()

    total = Decimal("0")

    for transaction in transactions:
        total += (transaction.amount * Decimal(str(EXCHANGE_RATES_TO_USD[transaction.currency])))

    return total


async def get_not_rollbacked_withdraw_amount(session: AsyncSession, dt_gt: date, dt_lt: date):
    q = (
        select(Transaction)
        .where(
            func.date(Transaction.created) >= dt_gt,
            func.date(Transaction.created) <= dt_lt,
            Transaction.amount < 0,
            Transaction.status != "ROLLBACKED",
            Transaction.is_active != False,
        )
    )

    result = await session.execute(q)
    transactions = result.scalars().all()

    total = Decimal("0")

    for transaction in transactions:
        total += (transaction.amount * Decimal(str(EXCHANGE_RATES_TO_USD[transaction.currency])))

    return total


async def get_transactions_count(session: AsyncSession, dt_gt: date, dt_lt: date)-> int:
    q = select(func.count(Transaction.id)).where(
        (func.date(Transaction.created) >= dt_gt) & (func.date(Transaction.created) <= dt_lt))
    result = await session.execute(q)
    return result.scalar_one()


async def get_not_rollbacked_transactions_count(session: AsyncSession, dt_gt: date, dt_lt: date)-> int:
    q = select(func.count(Transaction.id)).where(
        (func.date(Transaction.created) >= dt_gt) , (func.date(Transaction.created) <= dt_lt) ,(Transaction.status != "ROLLBACKED"), Transaction.is_active != False,)
    result = await session.execute(q)
    return result.scalar_one()
