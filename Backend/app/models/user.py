from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, text
from datetime import datetime

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
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