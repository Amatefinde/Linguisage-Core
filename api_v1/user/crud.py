from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.models import User, Session
from sqlalchemy.engine import Result
from .schemas import UserCreateSchema, UserUpdateSchema, SessionSchema
from ..auth_tools.auth import get_hashed_password


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)

    return await session.scalar(stmt)


async def add_user(session: AsyncSession, user: UserCreateSchema):
    user = user.model_dump()
    user["hash_password"] = get_hashed_password(user["password"])
    del user["password"]
    db_user = User(**user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user_partition(
    session: AsyncSession,
    user_id: int,
    new_user: UserUpdateSchema,
):
    user = await get_user_by_id(user_id=user_id, session=session)
    for name, value in new_user.model_dump(exclude_unset=True).items():
        if name == "password":
            name = "hash_password"
        setattr(user, name, value)

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()


async def add_user_session(session: AsyncSession, user_session: SessionSchema):
    user = await get_user_by_id(session=session, user_id=user_session.user_id)

    stmt = (
        select(Session)
        .where(Session.user_id == user_session.user_id)
        .where(Session.ip == user_session.ip)
        .where(Session.browser_header == user_session.browser_header)
    )
    db_session = await session.scalar(stmt)
    if db_session:
        db_session.token = user_session.token
        await session.commit()
        return await session.refresh(db_session)

    db_session = Session(**user_session.model_dump(), user=user)
    session.add(db_session)
    await session.commit()
    await session.refresh(db_session)

    print(
        "Вход с нового устройства: ", *list(user_session.model_dump().items()), sep="\n"
    )

    return db_session


async def delete_user_session(session: AsyncSession, user_session: SessionSchema):
    user = await get_user_by_id(session=session, user_id=user_session.user_id)
    db_session = Session(**user_session.model_dump(), user=user)
    await session.delete(db_session)
    await session.commit()
