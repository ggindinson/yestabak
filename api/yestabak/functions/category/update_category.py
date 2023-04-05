from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, Union


def update_category(
    session: Session, id: int, **new_category_data
) -> Tuple[Union[bool, None], Union[Category, str]]:
    try:
        new_category_data = dict(
            filter(lambda pair: pair[1] is not None, new_category_data.items())
        )
        session.query(Category).filter(Category.id == int(id)).update(new_category_data)
        session.commit()

        category = session.query(Category).filter(Category.id == int(id)).first()

        if not category:
            return (None, f"<Category id:{id}> doesn't exist!")

        return (True, category)
    except Exception as err:
        session.rollback()
        return (False, err)
