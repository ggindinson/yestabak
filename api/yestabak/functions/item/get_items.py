from sqlalchemy.orm import Session
from yestabak.models import Item
from typing import Tuple, Union, List


def get_items(
    session: Session,
) -> Tuple[bool, Union[List[Item], list, str]]:
    try:
        items = session.query(Item).all()
        session.close()

        if not items:
            return (True, [])

        return (True, items)
    except Exception as err:
        return (False, err)
