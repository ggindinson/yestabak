from sqlalchemy.orm import Session
from yestabak.models import User, Item
from typing import Tuple, Union, List


def get_cart_items(
    session: Session, telegram_id: int
) -> Tuple[bool, Union[List[Item], list, str]]:
    try:
        session.expire_on_commit = True
        user = session.query(User).get(telegram_id) # Replace with the telegram_id of the user you want to get the cart for
        cart_items = user.cart_items if user.cart_items else []
        session.close()
        return (True, cart_items)
    except Exception as err:
        return (False, err)
