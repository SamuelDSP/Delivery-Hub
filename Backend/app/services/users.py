from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate


async def get_user_by_id_service(db: AsyncSession, user_id: int) -> UserOut:
    user = await db.get(User, user_id)

    if user is None:
        return None

    return user

async def get_user_by_email_service(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if user is None:
        return None

    return user

async def get_user_by_identifier_service(
    db: AsyncSession,
    identifier: str,
) -> User | None:

    result = await db.execute(
        select(User).where(
            or_(
                User.email == identifier,
                User.username == identifier,
            )
        )
    )

    return result.scalars().first()

async def get_user_by_username_service(
    db: AsyncSession,
    username: str,
) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )

    return result.scalars().first()

