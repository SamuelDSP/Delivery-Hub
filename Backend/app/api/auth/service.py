from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import generate_hash
from app.core.exceptions import email_exists_exception
from app.services.users import get_user_by_email_service

async def register_user_service(db: AsyncSession,user_data: UserCreate) -> User | None:
    user_exists = await get_user_by_email_service(db, user_data.email)

    if user_exists:
        raise email_exists_exception

    hashed_password = generate_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )

    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        return None
    await db.refresh(new_user)

    return new_user