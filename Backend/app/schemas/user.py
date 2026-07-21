from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from app.core.enums import UserRole


class UserBase(BaseModel):
    username: str = Field(..., example="john_moe")
    email: str = Field(..., example="johnmoe@gmail.com")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=10,
        example="strongpassword123!",
    )
    role: UserRole

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if password.isalnum():
            raise ValueError("Password must contain at least one special character")

        return password

class UserOut(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, example="john_moe_updated")
    email: Optional[str] = Field(None, example="johnmoe@gmail.com")
    password: Optional[str] = Field(None, min_length=10, example="newstrongpassword123")
