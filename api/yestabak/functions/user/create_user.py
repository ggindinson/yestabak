from sqlalchemy.orm import Session
from yestabak.models import User
from typing import Tuple, Union


def create_user(
    session: Session, telegram_id, first_name, last_name, username, phone_number
) -> Tuple[bool, Union[User, str]]:
    try:
        user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        session.add(user)
        session.commit()

        user = (
            session.query(User)
            .filter(User.telegram_id == int(user.telegram_id))
            .first()
        )
        return (True, user)
    except Exception as err:
        session.rollback()
        return (False, err)
