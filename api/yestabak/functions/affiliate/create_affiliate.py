from sqlalchemy.orm import Session
from yestabak.models import Affiliate
from typing import Tuple, Union


def create_affiliate(
    session: Session, group_id, data
) -> Tuple[bool, Union[Affiliate, str]]:
    try:
        affiliate = Affiliate(group_id=group_id, data=data)
        session.add(affiliate)
        session.commit()

        affiliate = (
            session.query(Affiliate).filter(Affiliate.id == int(affiliate.id)).first()
        )
        session.close()
        return (True, affiliate)
    except Exception as err:
        session.rollback()
        return (False, err)
