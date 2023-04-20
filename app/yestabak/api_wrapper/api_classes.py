from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    created_at: str
    first_name: str
    last_name: Optional[str]
    last_updated_at: str
    phone_number: str
    role: str
    telegram_id: int
    username: Optional[str]


@dataclass
class CartItem:
    id: int
    item_id: int
    quantity: int
    telegram_id: int


@dataclass
class UserDataResponse:
    addresses: List[str]
    user: User
    cart: List[CartItem]
