from pydantic import BaseModel, Field
from typing import Optional

class UserLogin(BaseModel):
    identifier: str = Field(..., example="john_moe")
    password: str = Field(..., min_length=10, example="strongpassword123")

class TokenOut(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    refresh_token: str = Field(..., example="dGhpcy1pcz1hLXJlZnJlc2gtdG9rZW4...")
    token_type: str = Field(..., example="bearer")
    expires_in: int = Field(..., example=3600)

class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    exp: Optional[int] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., example="dGhpcy1pcz1hLXJlZnJlc2gtdG9rZW4...")