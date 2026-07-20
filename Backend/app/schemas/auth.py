from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    identifier: str = Field(
        ...,
        example="john_doe ou john@email.com"
    )
    password: str = Field(
        ...,
        min_length=8,
        example="strongpassword123"
    )


class TokenOut(BaseModel):
    access_token: str = Field(
        ...,
        example="eyJhbGciOiJIUzI1NiIs..."
    )
    token_type: str = Field(
        default="bearer",
        example="bearer"
    )
    expires_in: int = Field(
        ...,
        example=1800
    )


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str