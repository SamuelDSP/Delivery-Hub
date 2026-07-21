from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.enums import UserRole
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


async def create_order_service(db: AsyncSession, order_in: OrderCreate, current_user: User) -> Order:
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can place orders",
        )

    if not order_in.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    product_ids = [item.product_id for item in order_in.items]
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.seller))
        .where(Product.id.in_(product_ids))
    )
    products = {product.id: product for product in result.scalars().all()}

    if len(products) != len(set(product_ids)):
        raise HTTPException(status_code=404, detail="One or more products were not found")

    seller_ids = {product.seller_id for product in products.values()}
    if len(seller_ids) != 1:
        raise HTTPException(status_code=400, detail="Order items must be from the same seller")

    total = 0.0
    order_items = []

    for item in order_in.items:
        product = products[item.product_id]
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

        subtotal = product.price * item.quantity
        total += subtotal
        product.stock -= item.quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                subtotal=subtotal,
            )
        )

    order = Order(
        customer_id=current_user.id,
        seller_id=next(iter(seller_ids)),
        total=total,
        items=order_items,
    )

    db.add(order)
    await db.commit()

    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.seller),
            selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.seller),
        )
        .where(Order.id == order.id)
    )
    return result.scalars().first()


async def get_my_orders_service(db: AsyncSession, current_user: User) -> list[Order]:
    statement = select(Order).options(
        selectinload(Order.seller),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.seller),
    )

    if current_user.role == UserRole.CUSTOMER:
        statement = statement.where(Order.customer_id == current_user.id)
    elif current_user.role == UserRole.SELLER:
        statement = statement.where(Order.seller_id == current_user.id)

    result = await db.execute(statement.order_by(Order.created_at.desc()))
    return list(result.scalars().all())
