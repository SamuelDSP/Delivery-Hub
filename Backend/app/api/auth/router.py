from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import service
from app.db.deps import get_db

from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin, TokenOut
from app.api.auth.service import register_user_service, login_user_service
from app.core.exceptions import EmailExistsException, UsernameExistsException, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user_endpoint(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await register_user_service(db, user_data)

    except EmailExistsException:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    except UsernameExistsException:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

@router.post("/login", response_model=TokenOut)
async def login_endpoint(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await login_user_service(db, login_data)

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=401,
            detail="Invalid username/email or password",
        )