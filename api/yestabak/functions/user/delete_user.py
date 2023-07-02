from sqlalchemy.orm import Session
from yestabak.models import User
from typing import Tuple, Union


def delete_user(
    session: Session, telegram_id: int
) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        user = session.query(User).filter(User.telegram_id == int(telegram_id)).first()

        if not user:
            return (None, f"<User telegram_id:{telegram_id}> doesn't exist!")

        session.delete(user)
        session.commit()
        session.close()

        return (True, telegram_id)
    except Exception as err:
        session.rollback()
        return (False, err)
