from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, Union


def delete_category(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        category = session.query(Category).filter(Category.id == int(id)).first()

        if not category:
            return (None, f"<Category id:{id}> doesn't exist!")

        session.delete(category)
        session.commit()

        return (True, id)
    except Exception as err:
        session.rollback()
        return (False, err)
