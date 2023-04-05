from sqlalchemy.orm import Session, joinedload
from yestabak.models import Affiliate
from typing import Tuple, Union


def get_affiliate(
    session: Session, id: int
) -> Tuple[Union[bool, None], Union[Affiliate, str]]:
    try:
        affiliate = session.query(Affiliate).filter(Affiliate.id == int(id)).first()

        if not affiliate:
            return (None, f"<Affiliate id:{id}> doesn't exist!")

        return (True, affiliate)
    except Exception as err:
        return (False, err)
