from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Address:
    data: Dict[str, str | int] | None
    id: int


@dataclass
class CartItem:
    id: int
    name: str
    category_id: int
    created_at: str
    last_updated_at: str
    currency: str
    description: str
    price: int
    photo: str
    quantity: int


@dataclass
class Item:
    id: int
    name: str
    category_id: int
    created_at: str
    last_updated_at: str
    currency: str
    description: str
    price: int
    photo: str


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


@dataclass
class ImportedItem:
    name: str
    price: float

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
