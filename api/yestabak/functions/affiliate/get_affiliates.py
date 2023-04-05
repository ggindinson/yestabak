from sqlalchemy.orm import Session, joinedload
from yestabak.models import Affiliate
from typing import Tuple, Union, List


def get_affiliates(
    session: Session,
) -> Tuple[Union[bool, None], Union[List[Affiliate], str]]:
    try:
        affiliates = session.query(Affiliate).all()

        if not affiliates:
            return (True, [])

        return (True, affiliates)
    except Exception as err:
        return (False, err)
