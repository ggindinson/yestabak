from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union


def remove_cart_item(
    session: Session, item_id: int, telegram_id: int, **new_cart_data
) -> Tuple[Union[bool, None], Union[Cart, str]]:
    try:
        new_cart_data = dict(
            filter(lambda pair: pair[1] is not None, new_cart_data.items())
        )

        cart: Cart = (
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

        if cart.quantity <= 0:
            return (
                None,
                f"<Cart telegram_id:{telegram_id} item_id:{item_id}> doesn't exist!",
            )

        cart.quantity = int(cart.quantity) - 1
        session.add(cart)
        session.commit()

        cart: Cart = (
            session.query(Cart)
            .filter(
                Cart.telegram_id == int(telegram_id),
                Cart.item_id == int(item_id),
            )
            .first()
        )
        return (True, cart)
    except Exception as err:
        session.rollback()
        return (False, err)
