from sqlmodel import SQLModel, create_engine, Session
from lenny.configs import DB_URI, DEBUG

engine = create_engine(DB_URI, echo=DEBUG, client_encoding='utf8')


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
