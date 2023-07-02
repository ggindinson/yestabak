from sqlalchemy.orm import Session
from yestabak.models import Item
from typing import Tuple, Union


def delete_item(session: Session, id: int) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        item = session.query(Item).filter(Item.id == int(id)).first()

        if not item:
            return (None, f"<Item id:{id}> doesn't exist!")

        session.delete(item)
        session.commit()
        session.close()
        return (True, id)
    except Exception as err:
        session.rollback()
        return (False, err)
