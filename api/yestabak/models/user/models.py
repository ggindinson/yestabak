from typing import List
from sqlalchemy import Column, String, BigInteger, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from yestabak.core.db import Base


class User(Base):
    '''User'''

    __tablename__ = 'users'
    __table_args__ = {
        'extend_existing': True
    }  # redefine the table if it already exists

    telegram_id: Mapped[int] = mapped_column(
        nullable=False,
        primary_key=True,
        unique=True,
        comment='Уникальный user_id пользователя из телеграма',
    )
    
    role: Mapped[str] = mapped_column(default='user')
    
    first_name: Mapped[str] = mapped_column(comment='Имя пользователя')
    last_name: Mapped[str] = mapped_column(comment='Фамилия пользователя')
    username: Mapped[str] = mapped_column(nullable=True, comment='Юзернейм(псевдоним) пользователя')
    phone_number: Mapped[str] = mapped_column(nullable=True, comment='Номер телефона пользователя')

    addresses: Mapped[List['Address']] = relationship(back_populates='user', lazy='joined')
    cart_items: Mapped[List['CartItem']] = relationship(back_populates='user', lazy='joined')

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        comment="The date user was created at",
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
        comment="The date user was updated at",
    )
