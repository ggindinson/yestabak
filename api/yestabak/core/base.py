import sys
sys.path.append('/root/api')

from yestabak.core.db import SQLAlchemyBase, Base, engine
from yestabak.models import User, CartItem, Item, Address, Category, Affiliate


def create_all_tables():
    # If you want to create tables, just run this base.py file!
    SQLAlchemyBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all_tables()
