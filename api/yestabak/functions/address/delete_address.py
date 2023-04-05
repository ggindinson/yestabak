from sqlalchemy.orm import Session
from yestabak.models import Address
from typing import Tuple, Union


def delete_address(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        address = session.query(Address).filter(Address.id == int(id)).first()

        if not address:
            return (None, f"<Address id:{id}> doesn't exist!")

        session.delete(address)
        session.commit()

        return (True, id)
    except Exception as err:
        session.rollback()
        return (False, err)
