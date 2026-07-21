from datetime import datetime

from pydantic import BaseModel, Field

from app.models.order import OrderStatus
from app.schemas.product import ProductOut
from app.schemas.user import UserOut


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    product: ProductOut | None = None

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    customer_id: int
    seller_id: int
    status: OrderStatus
    total: float
    payment_provider: str | None = None
    payment_reference: str | None = None
    created_at: datetime
    updated_at: datetime
    seller: UserOut | None = None
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}
