from sqlalchemy.orm import Session, joinedload
from yestabak.models import User
from typing import Tuple, Union


def get_user(
    session: Session, telegram_id: int
) -> Tuple[Union[bool, None], Union[User, str]]:
    try:
        user = session.query(User).filter(User.telegram_id == int(telegram_id)).first()
        session.close()

        if not user:
            return (None, f"<User telegram_id:{telegram_id}> doesn't exist!")

        return (True, user)
    except Exception as err:
        return (False, err)
