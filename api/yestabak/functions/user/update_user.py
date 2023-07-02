from sqlalchemy.orm import Session
from yestabak.models import User
from typing import Tuple, Union


def update_user(
    session: Session, telegram_id: int, **new_user_data
) -> Tuple[Union[bool, None], Union[User, str]]:
    try:
        new_user_data = dict(
            filter(lambda pair: pair[1] is not None, new_user_data.items())
        )
        session.query(User).filter(User.telegram_id == int(telegram_id)).update(
            new_user_data
        )
        session.commit()

        user = session.query(User).filter(User.telegram_id == int(telegram_id)).first()
        session.close()

        if not user:
            return (None, f"<User telegram_id:{telegram_id}> doesn't exist!")

        return (True, user)
        # if new_user_data.get("telegram_id", None):
        #     user.telegram_id = new_user_data.get("telegram_id", user.telegram_id)

        # if new_user_data.get("first_name", None):
        #     user.first_name = new_user_data.get("first_name", user.first_name)

        # if new_user_data.get("last_name", None):
        #     user.last_name = new_user_data.get("last_name", user.last_name)

        # if new_user_data.get("username", None):
        #     user.username = new_user_data.get("username", user.username)

        # if new_user_data.get("phone_number", None):
        #     user.phone_number = new_user_data.get("phone_number", user.phone_number)
    except Exception as err:
        session.rollback()
        return (False, err)
