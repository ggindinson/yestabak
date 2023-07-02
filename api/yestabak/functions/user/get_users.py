from sqlalchemy.orm import Session
from yestabak.models import User
from typing import Tuple, Union, List


def get_users(session: Session) -> Tuple[bool, Union[List[User], list, str]]:
    try:
        users = session.query(User).all()
        session.close()

        if not users:
            return (True, [])

        return (True, users)
    except Exception as err:
        session.rollback()
        return (False, err)
