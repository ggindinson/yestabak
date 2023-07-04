from sqlalchemy.orm import Session
from yestabak.models import Category
from typing import Tuple, List, Union


def get_categories(session: Session) -> Tuple[bool, Union[List[Category], list, str]]:
    try:
        categories = session.query(Category).all()
        session.close()

        if not categories:
            return (True, [])

        return (True, categories)
    except Exception as err:
        session.rollback()
        return (False, err)
