from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.error_response import ErrorResponse
from app.schemas.user import UserOut, UserUpdate
from app.services.users import get_user_by_email_service, get_user_by_id_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/{user_id}",
    response_model=UserOut,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "error_code": "USER_NOT_FOUND",
                        "status": 404,
                    }
                }
            },
        }
    },
)
async def get_user_by_id_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id_service(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/email", response_model=UserOut)
async def get_user_by_email_endpoint(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email_service(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user