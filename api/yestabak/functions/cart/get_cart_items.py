from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union, List


def get_cart_items(
    session: Session, telegram_id: int
) -> Tuple[bool, Union[List[Cart], list, str]]:
    try:
        cart_items = (
            session.query(Cart).filter(Cart.telegram_id == int(telegram_id)).all()
        )

        if not cart_items:
            return (True, [])

        return (True, cart_items)
    except Exception as err:
        return (False, err)
