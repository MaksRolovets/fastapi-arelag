from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import RequestUserModel, UserStatusEnum

import datetime

async def get_all_users(session: AsyncSession,user_id: int | None = None, email: str | None = None, user_status: str | None = None):
    query =select(User).where(User.is_active == True)

    if user_id is not None:
        query = query.where(User.id == user_id)

    if email is not None:
        query = query.where(User.email == email)

    if user_status is not None:
        query = query.where(User.status == user_status)

    query = query.order_by(User.created.desc())
    result =  await session.execute(query)
    return result.scalars().all()

async def get_user_by_email(session: AsyncSession, user: RequestUserModel):
    return await session.execute(select(User).where(User.email==user.email))

async def get_user_by_id(session: AsyncSession, user_id : int):
    result =  await session.execute(select(User).where(User.id == user_id, User.is_active != False))
    return result.scalar()

async def create_user(session: AsyncSession, user: RequestUserModel):
    db_user = User(email=user.email, status="ACTIVE", created=datetime.datetime.utcnow())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def patch_user(session: AsyncSession, status: UserStatusEnum, user: User):
    user.status = status.value

    await session.commit()
    await session.refresh(user)

    return user