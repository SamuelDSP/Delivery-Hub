from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import service
from app.db.deps import get_db

from app.schemas.user import UserCreate
from app.api.auth.service import register_user_service
from app.core.exceptions import email_exists_exception

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user_endpoint(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user_service(db, user_data)
    except email_exists_exception:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    return user
