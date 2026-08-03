from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from schemas.analytics import TransactionAnalysisModel
from services.analytics import get_transaction_analysis_service

router = APIRouter(
    prefix="/transactions",
    tags=["Transaction"],
)


@router.get(
    "/analysis",
    response_model=list[TransactionAnalysisModel],
    status_code=status.HTTP_200_OK,
)
async def get_transaction_analysis(
    session: AsyncSession = Depends(get_async_session),
) -> list[TransactionAnalysisModel]:

    return await get_transaction_analysis_service(session)