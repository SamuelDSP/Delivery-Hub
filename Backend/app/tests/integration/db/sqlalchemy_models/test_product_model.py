import pytest
from sqlalchemy import select

from app.core.enums import UserRole
from app.models.product import Product
from app.models.user import User


async def create_seller(db_session, username="seller"):
    seller = User(
        username=username,
        email=f"{username}@example.com",
        hashed_password="hashed-password",
        role=UserRole.SELLER,
    )
    db_session.add(seller)
    await db_session.flush()
    await db_session.refresh(seller)
    return seller


@pytest.mark.asyncio
async def test_create_product(db_session):
    seller = await create_seller(db_session)

    product_data = {
        "name": "iPhone 15",
        "description": "Smartphone premium",
        "price": 4999.99,
        "stock": 50,
        "seller_id": seller.id,
    }

    new_product = Product(**product_data)
    db_session.add(new_product)
    await db_session.flush()
    await db_session.refresh(new_product)

    assert new_product.id is not None
    assert new_product.name == "iPhone 15"
    assert new_product.price == 4999.99
    assert new_product.stock == 50
    assert new_product.seller_id == seller.id
    assert new_product.created_at is not None


@pytest.mark.asyncio
async def test_product_validation(db_session):
    seller = await create_seller(db_session)

    product = Product(
        name="Product",
        description="Desc",
        price=100.0,
        stock=10,
        seller_id=seller.id,
    )
    db_session.add(product)
    await db_session.flush()

    assert product.price > 0
    assert product.stock >= 0


@pytest.mark.asyncio
async def test_product_relationships(db_session):
    seller = await create_seller(db_session)

    product = Product(
        name="Product with Category",
        description="Desc",
        price=50.0,
        stock=5,
        seller_id=seller.id,
    )
    db_session.add(product)
    await db_session.flush()
    await db_session.refresh(product)

    product_from_db = await db_session.get(Product, product.id)

    assert product_from_db is not None
    assert product_from_db.name == "Product with Category"
    assert product_from_db.seller_id == seller.id


@pytest.mark.asyncio
async def test_multiple_products(db_session):
    seller = await create_seller(db_session)

    products = [
        Product(
            name="Product A",
            description="Desc A",
            price=10.0,
            stock=5,
            seller_id=seller.id,
        ),
        Product(
            name="Product B",
            description="Desc B",
            price=20.0,
            stock=3,
            seller_id=seller.id,
        ),
        Product(
            name="Product C",
            description="Desc C",
            price=30.0,
            stock=8,
            seller_id=seller.id,
        ),
    ]

    for product in products:
        db_session.add(product)

    await db_session.flush()

    result = await db_session.execute(select(Product))
    all_products = list(result.scalars())
    assert len(all_products) == 3
