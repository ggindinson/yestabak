from sqlalchemy.orm import Session
from yestabak.models import Affiliate
from typing import Tuple, Union


def delete_affiliate(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[int, str]]:
    try:
        affiliate = session.query(Affiliate).filter(Affiliate.id == int(id)).first()

        if not affiliate:
            return (None, f"<Affiliate id:{id}> doesn't exist!")

        session.delete(affiliate)
        session.commit()
        session.close()

        return (True, id)
    except Exception as err:
        session.rollback()
        return (False, err)
