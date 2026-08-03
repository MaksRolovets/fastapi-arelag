from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from schemas.user import ResponseUserModel, RequestUserModel, UserModel, RequestUserUpdateModel
from services.user import get_users_service, create_user_service, patch_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get('',response_model=list[ResponseUserModel],status_code=status.HTTP_200_OK)
async def get_users(
    user_id: int | None = None,
    email: str | None = None,
    user_status: str | None = None,
    session: AsyncSession = Depends(get_async_session),
) -> list[ResponseUserModel]:
    return await get_users_service(session=session,user_id=user_id,email=email,user_status=user_status)

@router.post('', status_code=status.HTTP_200_OK)
async def post_user(user: RequestUserModel, session: AsyncSession = Depends(get_async_session)):
    return await create_user_service(session=session, user=user)

@router.patch("/{user_id}",response_model=UserModel,status_code=status.HTTP_200_OK,)
async def update_user_status(
    user_id: int,
    user: RequestUserUpdateModel,
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    return await patch_user_service(session=session,user_id=user_id,status_=user.status,)

