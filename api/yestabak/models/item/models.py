from typing import List
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from yestabak.core.db import Base


class Item(Base):
    """Item"""

    __tablename__ = "items"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the user",
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="cascade"),
        index=True,
        comment="ID of the item's category",
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    currency: Mapped[str] = mapped_column(nullable=False, default="RUB")
    photo: Mapped[str] = mapped_column(nullable=False)

    category: Mapped["Category"] = relationship(back_populates="items", lazy="joined")
    cart_items: Mapped[List["CartItem"]] = relationship(back_populates="item", cascade="delete, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        comment="The date item was created at",
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
        comment="The date item was updated at",
    )
