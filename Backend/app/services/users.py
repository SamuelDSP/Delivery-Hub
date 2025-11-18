from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserOut, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError

async def create_user_service(db: AsyncSession, user: UserCreate) -> UserOut:
    new_user = User(**user.model_dump())

    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        return None
    await db.refresh(new_user)
    
    return new_user


async def get_user_by_id_service(db: AsyncSession, user_id: int) -> UserOut:
    user = await db.get(User, user_id)

    if user is None:
        return None
    
    return user