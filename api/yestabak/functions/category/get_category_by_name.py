from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, Union


def get_category_by_name(
    session: Session, name: str
) -> Tuple[Union[bool, None], Union[Category, str]]:
    try:
        category = session.query(Category).filter(Category.name == str(name)).first()
        session.close()

        if not category:
            return (None, f"<Category name:{name}> doesn't exist!")

        return (True, category)
    except Exception as err:
        session.rollback()
        return (False, err)
