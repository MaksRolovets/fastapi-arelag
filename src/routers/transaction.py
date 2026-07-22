from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from db.database import get_async_session
from schemas.transaction import TransactionModel, RequestTransactionModel
from services.transaction import get_all_transactions_service, create_transaction_service, rollback_transaction_service

from exceptions.exceptions import BadRequestDataException

router = APIRouter(prefix="/transactions", tags=["Transaction"])


@router.get("", response_model=list[TransactionModel], status_code=status.HTTP_200_OK)
async def get_transactions(
    user_id: int | None = None,
    session: AsyncSession = Depends(get_async_session)
) -> list[TransactionModel]:

    results = await get_all_transactions_service(session, user_id)
    return results

@router.post("/{user_id}", response_model=TransactionModel | None, status_code=status.HTTP_200_OK)
async def post_transaction(user_id: int, transaction: RequestTransactionModel, session: AsyncSession = Depends(get_async_session)):
    return await create_transaction_service(session, user_id, transaction.currency, transaction.amount)

@router.patch("/{user_id}/transactions/{transaction_id}", response_model=TransactionModel | None, status_code=status.HTTP_200_OK)
async def patch_rollback_transaction(user_id: int, transaction_id: int, session: AsyncSession = Depends(get_async_session)):
    return await rollback_transaction_service(session, user_id, transaction_id)
    
    
    
