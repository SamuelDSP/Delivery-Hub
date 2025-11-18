from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(...,example="Sample Product")
    description: Optional[str] = Field(None, example="This is a sample product.")
    price: float = Field(..., gt=0, example=29.99)
    stock: int = Field(..., ge=0, example=100)

class ProductCreate(ProductBase):
    photo_url: Optional[str] = Field(None, example="http://example.com/photo.jpg")
    photo_mime_type: Optional[str] = Field(None, example="image/jpeg")
    photo_width: Optional[int] = Field(None, example=800)
    photo_height: Optional[int] = Field(None, example=600)
    photo_bytes_size: Optional[int] = Field(None, example=204800)
    photo_hash: Optional[str] = Field(None, example="abc123212def456ghi789")
    photo_file_name: Optional[str] = Field(None, example="toolphoto.jpg")
    photo_thumbnail_url: Optional[str] = Field(None, example="http://example.com/photo_thumbnail.jpg")

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None

    photo_url: Optional[str] = None
    photo_mime_type: Optional[str] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    photo_bytes_size: Optional[int] = None
    photo_hash: Optional[str] = None
    photo_file_name: Optional[str] = None
    photo_thumbnail_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Product Name")
    description: Optional[str] = Field(None, example="Updated description of the product.")
    price: Optional[float] = Field(None, gt=0, example=39.99)
    stock: Optional[int] = Field(None, ge=0, example=150)
    
    photo_url: Optional[str] = Field(None, example="http://example.com/updated_photo.jpg")
    photo_mime_type: Optional[str] = Field(None, example="image/png")
    photo_width: Optional[int] = Field(None, example=1024)
    photo_height: Optional[int] = Field(None, example=768)
    photo_bytes_size: Optional[int] = Field(None, example=307200)
    photo_hash: Optional[str] = Field(None, example="def456ghi789abc123212")
    photo_file_name: Optional[str] = Field(None, example="updatedphoto.png")
    photo_thumbnail_url: Optional[str] = Field(None, example="http://example.com/updated_photo_thumbnail.jpg")