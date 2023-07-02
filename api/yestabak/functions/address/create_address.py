from sqlalchemy.orm import Session
from yestabak.models import Address
from typing import Tuple, Union


def create_address(
    session: Session, telegram_id, data
) -> Tuple[bool, Union[Address, str]]:
    try:
        address = Address(user_id=telegram_id, data=data)
        session.add(address)
        session.commit()

        address = session.query(Address).filter(Address.id == int(address.id)).first()
        session.close()
        return (True, address)
    except Exception as err:
        session.rollback()
        return (False, err)
