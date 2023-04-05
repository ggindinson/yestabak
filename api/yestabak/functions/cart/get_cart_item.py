from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union, List


def get_cart_item(
    session: Session, telegram_id: int, item_id: int
) -> Tuple[bool, Union[List[Cart], list, str]]:
    try:
        cart_item: Cart = (
            session.query(Cart)
            .filter(Cart.telegram_id == int(telegram_id), Cart.item_id == int(item_id))
            .first()
        )

        if not cart_item:
            return (
                None,
                f"<Cart telegram_id:{telegram_id} item_id:{item_id}> doesn't exist!",
            )

        return (True, cart_item)
    except Exception as err:
        return (False, err)
