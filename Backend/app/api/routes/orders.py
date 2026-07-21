from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.services.order import create_order_service, get_my_orders_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut)
async def create_order_endpoint(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_order_service(db, order_in, current_user)


@router.get("/", response_model=list[OrderOut])
async def get_my_orders_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_my_orders_service(db, current_user)
