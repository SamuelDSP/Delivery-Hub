from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin, TokenOut
from app.core.security import generate_hash, verify_password, create_access_token
from app.core.exceptions import email_exists_exception
from app.services.users import get_user_by_email_service, get_user_by_username_service, get_user_by_identifier_service
from app.core.exceptions import EmailExistsException, UsernameExistsException, InvalidCredentialsException
from app.core.config import settings

async def register_user_service(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:

    email_exists = await get_user_by_email_service(
        db,
        user_data.email,
    )

    if email_exists:
        raise EmailExistsException()

    username_exists = await get_user_by_username_service(
        db,
        user_data.username,
    )

    if username_exists:
        raise UsernameExistsException()

    hashed_password = generate_hash(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=UserRole.CUSTOMER,
    )

    db.add(new_user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(new_user)

    return new_user

async def login_user_service(
    db: AsyncSession,
    login_data: UserLogin,
) -> TokenOut:

    user = await get_user_by_identifier_service(
        db,
        login_data.identifier,
    )

    if user is None:
        raise InvalidCredentialsException()

    if not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise InvalidCredentialsException()

    access_token = create_access_token(
        {
            "sub": str(user.id),
        }
    )

    return TokenOut(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
