from yestabak.core.db import SQLAlchemyBase, Base
from yestabak.models import User, Cart, Item, Address, Category, Affiliate


def create_all_tables():
    # If you want to create tables, just run this base.py file!
    SQLAlchemyBase.metadata.create_all()


if __name__ == "__main__":
    create_all_tables()
