from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:qwerty123456@localhost:5432/yestabak"
)

# Create engine with postgresql connection uri
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


# Get default sqlalchemy model's class to extend it soon
SQLAlchemyBase = declarative_base()


# Extend 'SQLAlchemyBase' class with our new 'Base' class.
class Base(SQLAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        try:
            return "<class '{}' telegram_id:{}>".format(
                self.__class__.__name__, self.telegram_id
            )
        except:
            return "<class '{}' id:{}>".format(self.__class__.__name__, self.id)
