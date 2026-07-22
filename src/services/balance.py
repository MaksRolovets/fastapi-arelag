from sqlalchemy.ext.asyncio import AsyncSession
from schemas.transaction import TransactionStatusEnum, TransactionModel
from schemas.enums import CurrencyEnum
from repositories.transaction import get_all_transactions
from fastapi import  status

from repositories.balance import get_balance_user_id

from exceptions.exceptions import BadRequestDataException, UserNotExistsException, CreateTransactionForBlockedUserException


# async def get_user_balance_service(session: AsyncSession, user_id : int, currency : CurrencyEnum | None = None,):
#     db_user_balance = await get_balance_user_id(session, user_id, currency)
#     if float(db_user_balance.amount) + transaction.amount < 0:
#         raise NegativeBalanceException(status_code=status.HTTP_400_BAD_REQUEST, detail="Negative balance")