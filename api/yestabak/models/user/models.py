from sqlalchemy import Column, String, BigInteger, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from yestabak.core.db import Base


class User(Base):
    """User"""

    __tablename__ = "users"
    __table_args__ = {
        "extend_existing": True
    }  # redefine the table if it already exists

    telegram_id = Column(
        BigInteger,
        nullable=False,
        primary_key=True,
        unique=True,
        comment="Уникальный user_id пользователя из телеграма",
    )
    
    role = Column(String, default="user")
    
    first_name = Column(String, comment="Имя пользователя")
    last_name = Column(String, comment="Фамилия пользователя")
    username = Column(String, nullable=True, comment="Юзернейм(псевдоним) пользователя")
    phone_number = Column(String, nullable=True, comment="Номер телефона пользователя")

    addresses = relationship("Address", back_populates="user", lazy="joined")

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        comment="Дата создания пользователя",
    )
    last_updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
        comment="Дата последнего обновления данных пользователя",
    )
