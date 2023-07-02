from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, Union


def get_category(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[Category, str]]:
    try:
        category = session.query(Category).filter(Category.id == int(id)).first()
        session.close()

        if not category:
            return (None, f"<Category id:{id}> doesn't exist!")

        return (True, category)
    except Exception as err:
        session.rollback()
        return (False, err)
