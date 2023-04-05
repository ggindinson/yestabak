from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union, List


def delete_cart_items(
    session: Session, item_id: int, telegram_id: int
) -> Tuple[bool, Union[List[int], list, str]]:
    try:
        cart_items = (
            session.query(Cart).filter(Cart.telegram_id == int(telegram_id)).all()
        )

        if not cart:
            return (True, [])

        item_ids = [item.item_id for item in cart_items]

        session.delete(cart)
        session.commit()

        return (True, item_ids)
    except Exception as err:
        session.rollback()
        return (False, err)
