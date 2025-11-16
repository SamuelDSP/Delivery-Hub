from typing import Optional
from datetime import datetime
from app.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, text


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    created_by_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    photo_mime_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    photo_width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_bytes_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    photo_file_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    photo_thumbnail_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

