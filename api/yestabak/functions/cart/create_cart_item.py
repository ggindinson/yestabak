from sqlalchemy.orm import Session
from yestabak.models import Cart
from typing import Tuple, Union
from .update_cart_item import update_cart_item


def create_cart_item(
    session: Session, telegram_id: int, item_id: int
) -> Tuple[bool, Union[Cart, str]]:
    try:
        cart: Cart = (
            session.query(Cart)
            .filter(Cart.telegram_id == int(telegram_id), Cart.item_id == int(item_id))
            .first()
        )

        if cart:
            ret = update_cart_item(
                session=session,
                item_id=item_id,
                telegram_id=telegram_id,
                quantity=int(cart.quantity) + 1,
            )
            return ret

        cart = Cart(
            telegram_id=telegram_id,
            item_id=item_id,
        )
        session.add(cart)
        session.commit()

        cart = session.query(Cart).filter(Cart.id == int(cart.id)).first()
        return (True, cart)
    except Exception as err:
        session.rollback()
        return (False, err)
