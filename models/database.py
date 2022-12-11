from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base




DATABASE_NAME = 'hotels2.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
base = declarative_base()


def create_db():
    base.metadata.create_all(engine)
