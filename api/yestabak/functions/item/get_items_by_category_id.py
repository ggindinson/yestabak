from sqlalchemy.orm import Session
from yestabak.models import Item, Category
from typing import Tuple, Union, List


def get_items_by_category_id(
    session: Session, category_id: int
) -> Tuple[Union[bool, None], Union[List[Item], list, str]]:
    try:
        category = (
            session.query(Category).filter(Category.id == int(category_id)).first()
        )

        if not category:
            return (None, f"<Category id:{category_id}> doesn't exist!")

        items_by_category_id = (
            session.query(Item).filter(Item.category_id == int(category_id)).all()
        )
        session.close()

        if not items_by_category_id:
            return (True, [])

        return (True, items_by_category_id)
    except Exception as err:
        return (False, err)
