from sqlalchemy.orm import Session, joinedload
from yestabak.models import Address
from typing import Tuple, Union


def get_address(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[Address, str]]:
    try:
        address = session.query(Address).filter(Address.id == int(id)).first()

        if not address:
            return (None, f"<Address id:{id}> doesn't exist!")

        return (True, address)
    except Exception as err:
        return (False, err)
