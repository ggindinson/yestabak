from sqlalchemy.orm import Session
from yestabak.models import Item
from typing import Tuple, Union


def update_item(
    session: Session, id: int, **new_item_data
) -> Tuple[Union[bool, None], Union[Item, str]]:
    try:
        new_item_data = dict(
            filter(lambda pair: pair[1] is not None, new_item_data.items())
        )
        session.query(Item).filter(Item.id == int(id)).update(new_item_data)
        session.commit()

        item = session.query(Item).filter(Item.id == int(id)).first()
        session.close()

        if not item:
            return (None, f"<Item id:{id}> doesn't exist!")

        return (True, item)

        # if new_item_data.get("category_id", None):
        #     item.category_id = new_item_data.get("category_id", item.category_id)

        # if new_item_data.get("name", None):
        #     item.name = new_item_data.get("name", item.name)

        # if new_item_data.get("description", None):
        #     item.description = new_item_data.get("description", item.description)

        # if new_item_data.get("price", None):
        #     item.price = new_item_data.get("price", item.price)

        # if new_item_data.get("photo", None):
        #     item.photo = new_item_data.get("photo", item.photo)

        # session.add(item)

        # item = session.query(Item).filter(Item.id == int(item.id)).first()
    except Exception as err:
        session.rollback()
        return (False, err)
