from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from yestabak.core.db import Base
from typing import List


class Category(Base):
    """Категория товаров"""

    __tablename__ = "categories"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the category",
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        comment="Название категории",
    )

    items: Mapped[List["Item"]] = relationship(back_populates="category", lazy="joined", cascade="delete, delete-orphan")
