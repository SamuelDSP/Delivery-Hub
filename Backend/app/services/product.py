from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate


async def create_product_service(
    db: AsyncSession, product: ProductCreate
) -> ProductOut:
    new_product = Product(**product.model_dump(exclude_unset=True))

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
    db: AsyncSession, product_id: int, product_in: ProductUpdate
) -> ProductOut:
    product = await db.get(Product, product_id)
    if product == None:
        return None

    data = product_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(product, key, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


async def delete_product_service(db: AsyncSession, product_id: int) -> bool:
    product = await db.get(Product, product_id)
    if product == None:
        return False
    await db.delete(product)
    await db.commit()
    return True
