from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.database import Base
from os import path

sqlite_path = path.join(path.dirname(__file__), "sqlite.db")
engine = create_engine(f"sqlite:///{sqlite_path}", convert_unicode=True)

db_session = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine
)
scoped_session = scoped_session(db_session)


def get_session():
	return db_session()


def init_db():
	from src.database import Exercise
	Base.metadata.create_all(engine)
