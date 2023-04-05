from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, Union


def create_category(session: Session, name: str) -> Tuple[bool, Union[Category, str]]:
    try:
        category = Category(name=name)
        session.add(category)
        session.commit()

        category = (
            session.query(Category).filter(Category.id == int(category.id)).first()
        )
        return (True, category)
    except Exception as err:
        session.rollback()
        return (False, err)
