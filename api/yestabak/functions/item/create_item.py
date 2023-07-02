from sqlalchemy.orm import Session
from yestabak.models import Item
from typing import Tuple, Union


def create_item(
    session: Session, category_id, name, description, price, photo
) -> Tuple[bool, Union[Item, str]]:
    try:
        item = Item(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            photo=photo,
        )
        session.add(item)
        session.commit()

        item = session.query(Item).filter(Item.id == int(item.id)).first()
        session.close()
        return (True, item)
    except Exception as err:
        session.rollback()
        return (False, err)
