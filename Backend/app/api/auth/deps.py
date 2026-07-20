from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from Backend.app.core.enums import UserRole
from Backend.app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.jwt import decode_access_token
from app.db.deps import get_db
from app.schemas.auth import TokenPayload
from app.services.users import get_user_by_id_service


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        token_data = TokenPayload(**payload)

    except JWTError:
        raise credentials_exception

    if token_data.sub is None:
        raise credentials_exception

    user = await get_user_by_id_service(
        db,
        int(token_data.sub),
    )

    if user is None:
        raise credentials_exception

    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )

    return current_user

async def get_current_admin_or_seller(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.SELLER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator or seller access required",
        )

    return current_user

async def get_current_admin_or_customer(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.CUSTOMER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator or customer access required",
        )

    return current_user