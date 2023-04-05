from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union


def update_cart_item(
    session: Session, item_id: int, telegram_id: int, **new_cart_data
) -> Tuple[Union[bool, None], Union[Cart, str]]:
    try:
        new_cart_data = dict(
            filter(lambda pair: pair[1] is not None, new_cart_data.items())
        )

        session.query(Cart).filter(
            Cart.telegram_id == int(telegram_id),
            Cart.item_id == int(item_id),
        ).update(new_cart_data)
        session.commit()

        cart = (
            session.query(Cart)
            .filter(
                Cart.telegram_id == int(telegram_id),
                Cart.item_id == int(item_id),
            )
            .first()
        )
        if not cart:
            return (
                None,
                f"<Cart telegram_id:{telegram_id} item_id:{item_id}> doesn't exist!",
            )

        return (True, cart)
    except Exception as err:
        session.rollback()
        return (False, err)
