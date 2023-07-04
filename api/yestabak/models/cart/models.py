from typing import List
from sqlalchemy import ForeignKey, Column, String, Integer, Text, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from yestabak.core.db import Base


class CartItem(Base):
    """Ассоциативная таблица для связи пользователя и корзин с товарами"""

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the cart item",
    )
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="cascade"),
        nullable=True,
        index=True,
        comment="Уникальный идентификатор юзера",
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="cascade"),
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор товара",
    )
    quantity: Mapped[int] = mapped_column(default=1, comment="Количество товара")

    user: Mapped["User"] = relationship(back_populates="cart_items")
    item: Mapped["Item"] = relationship(back_populates="cart_items", lazy="joined")
