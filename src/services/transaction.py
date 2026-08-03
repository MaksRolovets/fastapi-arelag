from sqlalchemy.ext.asyncio import AsyncSession
from schemas.transaction import TransactionStatusEnum, TransactionModel
from schemas.enums import CurrencyEnum
from repositories.transaction import get_all_transactions, create_transaction, get_transactions_by_id, update_transaction
from repositories.balance import get_balance_user_id, update_user_balance
from decimal import Decimal
from fastapi import  status

from repositories.user import get_user_by_id

from exceptions.exceptions import(BadRequestDataException,
                                   UserNotExistsException,
                                     CreateTransactionForBlockedUserException,
                                       NegativeBalanceException,
                                       TransactionAlreadyRollbackedException,
                                       TransactionDoesNotBelongToUserException,
                                       TransactionNotExistsException,
                                       UpdateTransactionForBlockedUserException
                                       ) 


async def get_all_transactions_service(session : AsyncSession, user_id: int | None = None):
    results = []
    transactions = await get_all_transactions(session, user_id)
    for t in transactions:
        result = TransactionModel(
            **{
                "id": t.id,
                "user_id": t.user_id,
                "currency":CurrencyEnum(t.currency),
                "amount": t.amount,
                "status": TransactionStatusEnum(t.status),
                "created": t.created
            }
        )
        results.append(result)
    return results

async def create_transaction_service(session : AsyncSession,user_id : int,  currency: CurrencyEnum , amount: float ):
    if user_id < 0:
        raise BadRequestDataException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable data in request")
    if amount == 0:
        raise BadRequestDataException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Transaction can not have zero amount")

    db_user = await get_user_by_id(session, user_id)
    if not db_user: # оставить в сервисах или в репозиторий внести
        raise UserNotExistsException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id=`{0}` does not exist".format(user_id))
    if db_user.status != "ACTIVE":
        raise CreateTransactionForBlockedUserException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id=`{0}` is blocked".format(user_id))

    db_user_balance = await get_balance_user_id(session, user_id, currency)
    if db_user_balance.amount + amount < 0:
        raise NegativeBalanceException(status_code=status.HTTP_400_BAD_REQUEST, detail="Negative balance")

    await update_user_balance(session,db_user_balance,amount)
    db_transaction = await create_transaction(session, user_id, currency, amount)
    await session.commit()
    return TransactionModel(
        id=db_transaction.id,
        user_id=db_transaction.user_id,
        currency=CurrencyEnum(db_transaction.currency),
        amount=db_transaction.amount,
        status=TransactionStatusEnum(db_transaction.status),
        created=db_transaction.created,
    )

async def rollback_transaction_service(session: AsyncSession, user_id : int,  transaction_id: int):
    if user_id < 0 or transaction_id < 0:
        raise BadRequestDataException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable data in request")

    db_user = await get_user_by_id(session, user_id)
    if not db_user:
        raise UserNotExistsException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id=`{0}` does not exist".format(user_id))

    db_transaction = await get_transactions_by_id(session, transaction_id)
    if not db_transaction:
        raise TransactionNotExistsException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction with id=`{0}` does not exist".format(transaction_id)
        )
    if db_transaction.user_id != db_user.id:
        raise TransactionDoesNotBelongToUserException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction with id=`{0}` does not belong to user with id=`{1}`".format(transaction_id, user_id)
        )
    if db_transaction.status == "ROLLBACKED":
        raise TransactionAlreadyRollbackedException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction with id=`{0}` is already rollbacked".format(transaction_id)
        )

    if db_user.status == "BLOCKED":
        raise UpdateTransactionForBlockedUserException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with id=`{0}` is blocked".format(user_id)
        )

    db_user_balance = await get_balance_user_id(session, user_id, db_transaction.currency)
    rollback_amount = -db_transaction.amount

    if db_user_balance.amount + rollback_amount < Decimal("0"):
        raise NegativeBalanceException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Negative balance",
        )

    await update_user_balance(session, db_user_balance, rollback_amount)
    await update_transaction(session, db_transaction, TransactionStatusEnum.roll_backed)
    await session.commit()
    