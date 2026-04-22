from sqlalchemy import select
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