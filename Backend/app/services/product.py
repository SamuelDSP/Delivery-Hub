from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.user import User, UserRole
from fastapi import HTTPException, status
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate


async def create_product_service(
    db: AsyncSession, product: ProductCreate, current_user: User,
) -> ProductOut:
    new_product = Product(**product.model_dump(exclude_unset=True), seller_id=current_user.id)

    db.add(new_product)
    try:
        await db.commit()
    except IntegrityError:
        return None
    await db.refresh(new_product)

    return new_product


async def get_product_by_id_service(db: AsyncSession, product_id: int) -> ProductOut:
    product = await db.get(Product, product_id)

    if product is None:
        return None

    return product


async def update_product_service(
    db: AsyncSession,
    product_id: int,
    product_in: ProductUpdate,
    current_user: User,
) -> ProductOut:

    product = await db.get(Product, product_id)

    if product is None:
        return None

    if (
        current_user.role == UserRole.SELLER
        and product.seller_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own products",
        )

    data = product_in.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(product, key, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


async def delete_product_service(
    db: AsyncSession,
    product_id: int,
    current_user: User,
) -> bool:

    product = await db.get(Product, product_id)

    if product is None:
        return False

    if (
        current_user.role == UserRole.SELLER
        and product.seller_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own products",
        )

    await db.delete(product)
    await db.commit()

    return True


async def get_all_products_service(db: AsyncSession) -> list[ProductOut]:
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products