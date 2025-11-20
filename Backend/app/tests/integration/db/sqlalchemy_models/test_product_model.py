import pytest
from app.models.product import Product
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_product(db_session):
    
    product_data = {
        "name": "iPhone 15",
        "description": "Smartphone premium",
        "price": 4999.99,
        "stock": 50
    }
    
    new_product = Product(**product_data)
    db_session.add(new_product)
    await db_session.flush()
    await db_session.refresh(new_product)
    
    assert new_product.id is not None
    assert new_product.name == "iPhone 15"
    assert new_product.price == 4999.99
    assert new_product.stock == 50
    assert new_product.created_at is not None


@pytest.mark.asyncio
async def test_product_validation(db_session):
    
    product = Product(name="Produto Válido", description="Desc", price=100.0, stock=10)
    db_session.add(product)
    await db_session.flush()
    
    assert product.price > 0
    assert product.stock >= 0


@pytest.mark.asyncio
async def test_product_relationships(db_session):
    
    product = Product(name="Produto com Categoria", description="Desc", price=50.0, stock=5)
    db_session.add(product)
    await db_session.flush()
    await db_session.refresh(product)
    
    product_from_db = await db_session.get(Product, product.id)
    
    assert product_from_db is not None
    assert product_from_db.name == "Produto com Categoria"


@pytest.mark.asyncio
async def test_multiple_products(db_session):
    
    products = [
        Product(name="Produto A", description="Desc A", price=10.0, stock=5),
        Product(name="Produto B", description="Desc B", price=20.0, stock=3),
        Product(name="Produto C", description="Desc C", price=30.0, stock=8)
    ]
    
    for product in products:
        db_session.add(product)
    
    await db_session.flush()
    
    result = await db_session.execute(select(Product))
    all_products = list(result.scalars())
    assert len(all_products) == 3