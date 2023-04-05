from sqlalchemy import ForeignKey, Column, String, Integer, Text, DateTime, BigInteger
from sqlalchemy.orm import relationship
from yestabak.core.db import Base


class Cart(Base):
    """Корзина пользователя"""

    __tablename__ = "carts"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the cart",
    )

    telegram_id = Column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="cascade"),
        index=True,
        comment="Уникальный телеграм-идентификатор пользователя",
    )
    user = relationship("User", lazy="joined")

    item_id = Column(
        Integer,
        ForeignKey("items.id", ondelete="cascade"),
        comment="Уникальный идентификатор товара",
    )
    item = relationship("Item", lazy="joined")

    quantity = Column(BigInteger, comment="Количество товаров", default=1)
