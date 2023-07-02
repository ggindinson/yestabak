from sqlalchemy.orm import Session
import sqlalchemy as sa
from sqlalchemy import delete
from yestabak.models import User, Item, CartItem
from typing import Tuple, Union, List, Dict


def update_cart_items(
    session: Session,
    telegram_id: Union[int, str],
    items: List[Dict[str, Union[str, int, float]]],
):
    session.expire_on_commit = True
    # try:
    # Load the User instance for the specified user
    user = session.query(User).filter_by(telegram_id=telegram_id).one()
    
    # Clear the user's cart
    user.cart_items = []

    item_ids = []

    for item in items:
        try:
            is_item_exists = session.execute(sa.select(Item).where(Item.id == item['item_id'])).unique().scalar()
            print("telegram_id:", telegram_id, "\ncart_item:", is_item_exists)
            if is_item_exists and telegram_id:
                cart_item = CartItem(item_id=item["item_id"], quantity=item["quantity"])
                user.cart_items.append(
                    cart_item
                )
                item_ids.append(cart_item.item_id)
        except Exception as err:
            print(str(err))
            continue

    # print(user.cart_items[0].quantity)

    session.add(user)
    session.commit()
    
    # Commit the changes to the session
    user = session.execute(sa.select(User).where(User.telegram_id == telegram_id)).unique().scalar_one()
    cart_items = user.cart_items
    session.close()

    # Return the list of CartItem objects in the updated Cart instance
    return (True, cart_items)
    # except Exception as err:
    #     return (False, str(err))
