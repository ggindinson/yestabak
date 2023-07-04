from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Text,
    DateTime,
    BigInteger,
    DateTime,
    JSON,
)
from sqlalchemy.orm import relationship
from yestabak.core.db import Base


class Address(Base):
    """Адрес пользователя"""

    __tablename__ = "addresses"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        comment="ID of the address",
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="cascade"),
        comment="Уникальный телеграм-идентификатор пользователя",
    )

    user = relationship("User", back_populates="addresses")

    data = Column(
        JSON(),
        nullable=True,
        comment="Точный адрес найденный путём поиска через API (Яндекс Карты / Google Карты / OpenStreetMap) по введенному пользователем адресу.",
    )

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        comment="Дата создания адреса",
    )

    last_updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
        comment="Дата последнего обновления данных адреса",
    )
