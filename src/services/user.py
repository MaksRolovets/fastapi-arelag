from sqlalchemy.ext.asyncio import AsyncSession
from repositories.balance import get_users_balances,create_user_balance
from repositories.user import get_all_users,create_user, get_user_by_email, patch_user, get_user_by_id
from schemas.user import ResponseUserBalanceModel, ResponseUserModel, RequestUserModel, UserModel
from schemas.enums import UserStatusEnum
from exceptions.exceptions import UserAlreadyExistsException, BadRequestDataException, UserAlreadyActiveException, UserAlreadyBlockedException, UserNotExistsException
from fastapi import status

async def get_users_service(session: AsyncSession, user_id: int | None = None, email: str | None = None, user_status: str | None = None):
    users = await get_all_users(session, user_id, email, user_status)
    users_ids = []
    for user in users:
        users_ids.append(user.id)
    balances = await get_users_balances(session, users_ids)
    balances_map: dict[int, list[ResponseUserBalanceModel]] = {}

    for balance in balances:
        if balance.user_id not in balances_map:
            balances_map[balance.user_id] = []

        balances_map[balance.user_id].append(ResponseUserBalanceModel(currency=balance.currency,amount=balance.amount))

    result: list[ResponseUserModel] = []

    for user in users:
        result.append(
            ResponseUserModel(
                id=user.id,
                email=user.email,
                status=UserStatusEnum(user.status),
                created=user.created,
                balances=balances_map.get(user.id, [])
            ))
        
    return result

async def create_user_service(session: AsyncSession, user : RequestUserModel):
    if user is None:
        raise BadRequestDataException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email can't consist entirely of spaces")
    
    db_user = await get_user_by_email(session, user)
    if db_user.scalar():
        raise UserAlreadyExistsException(status_code=status.HTTP_409_CONFLICT, detail="User with email=`{0}` already exists".format(user.email))

    db_user = await create_user(session, user)
    await create_user_balance(session, user_id=db_user.id)
    return UserModel(
        id=db_user.id,
        email=db_user.email,
        status=UserStatusEnum(db_user.status),
        created=db_user.created
    )

async def patch_user_service(session: AsyncSession, status_ :UserStatusEnum, user_id : int):
    if user_id < 0:
        raise BadRequestDataException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable data in request")

    db_user = await get_user_by_id(session, user_id)

    if not db_user:
        raise UserNotExistsException(status_code=status.HTTP_404_NOT_FOUND, detail="User with id=`{0}` does not exist".format(user_id))
    
    if db_user.status == UserStatusEnum.BLOCKED.value and status_ == UserStatusEnum.BLOCKED:
        raise UserAlreadyBlockedException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id=`{user_id}` is already blocked",
        )

    if db_user.status == UserStatusEnum.ACTIVE.value and status_ == UserStatusEnum.ACTIVE:
        raise UserAlreadyActiveException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id=`{user_id}` is already active",
        )
    
    db_user =  await patch_user(session,status_, db_user)

    return UserModel(
        id=db_user.id,
        email=db_user.email,
        status =db_user.status,
        created=db_user.created,
    )
