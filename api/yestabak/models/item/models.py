from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from yestabak.core.db import Base


class Item(Base):
    """Item"""

    __tablename__ = "items"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)

    category_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="cascade"),
        comment="Уникальный идентификатор категории товара",
    )
    category = relationship("Category", back_populates="items")

    name = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    photo = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        comment="Дата создания товара",
    )
    last_updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
        comment="Дата последнего обновления данных товара",
    )
