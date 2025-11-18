from app.db.deps import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.services.product import (
    create_product_service,
    get_product_by_id_service,
    update_product_service,
    delete_product_service)

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductOut)
async def create_product_endpoint(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await create_product_service(db, product)

    if product is None:
        raise HTTPException(status_code=400, detail="Product with given details already exists")
    
    return product


@router.get("/{product_id}", response_model=ProductOut)
async def get_product_by_id_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id_service(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product_endpoint(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await update_product_service(db, product_id, product)

    if product == None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    delete = await delete_product_service(db, product_id)

    if not delete:
        raise HTTPException(status_code=404, detail="Product not found")