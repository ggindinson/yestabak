from sqlalchemy.orm import Session
from yestabak.models import Item
from typing import Tuple, Union


def get_item(session: Session, id: int) -> Tuple[Union[bool, None], Union[Item, str]]:
    try:
        item = session.query(Item).filter(Item.id == int(id)).first()
        session.close()

        if not item:
            return (None, f"<Item id:{id}> doesn't exist!")

        return (True, item)
    except Exception as err:
        session.rollback()
        return (False, err)
