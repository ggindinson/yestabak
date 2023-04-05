from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship
from yestabak.core.db import Base


class Category(Base):
    """Категория товаров"""

    __tablename__ = "categories"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the category",
    )

    name = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="Название категории",
    )

    items = relationship("Item", back_populates="category", lazy="joined")
