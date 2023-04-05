from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union


def delete_cart_item(
    session: Session, item_id: int, telegram_id: int
) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        cart = (
            session.query(Cart)
            .filter(Cart.telegram_id == int(telegram_id), Cart.item_id == int(item_id))
            .first()
        )

        if not cart:
            return (
                None,
                f"<Cart telegram_id:{telegram_id} item_id:{item_id}> doesn't exist!",
            )

        session.delete(cart)
        session.commit()

        return (True, item_id)
    except Exception as err:
        session.rollback()
        return (False, err)
