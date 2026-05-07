from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    Numeric,
    func, BigInteger
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship, declarative_mixin,
)

from src.database import Base

@declarative_mixin
class BaseMixin:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

class User(Base, BaseMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    banned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    ban_reason: Mapped[str] = mapped_column(String(100), nullable=True)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    role: Mapped["Role"] = relationship(
        back_populates="users",
    )

    products: Mapped[list["Product"]] = relationship(back_populates="creator")



class Role(Base, BaseMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
    )

class Category(Base, BaseMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        cascade="all, delete",
        passive_deletes=True,
    )

class Product(Base, BaseMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    price_rub: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    common_note: Mapped[str | None] = mapped_column(
        Text,
    )

    special_note: Mapped[str | None] = mapped_column(
        Text,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False, index=True,
    )


    category: Mapped["Category"] = relationship(
        back_populates="products",
    )

    creator: Mapped["User"] = relationship(
        back_populates="products",
    )