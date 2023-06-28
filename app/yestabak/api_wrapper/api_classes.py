from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Address:
    id: int | None
    address: str
    data: Dict[Any, Any] | None


@dataclass
class CartItem:
    id: int
    category_id: int
    created_at: str
    last_updated_at: str
    currency: str
    description: str
    price: int
    photo: str
    quantity: int


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
class UserDataResponse:
    addresses: List[Address]
    user: User
    cart_items: List[CartItem]
