from sqlalchemy import create_engine
from sqlalchemy.sql.ddl import DropSchema
from sqlalchemy.orm import scoped_session, sessionmaker
from src.database import Base
from os import path


# sqlite_path = path.join(path.dirname(__file__), "sqlite.db")
# engine = create_engine(f"sqlite:///{sqlite_path}", convert_unicode=True)
db_username = "postgres"
db_password = "c4rls4g4n"
db_endpoint = "database-1.cz7oddmvnfyc.us-east-1.rds.amazonaws.com"
db_name = "setsdatabase"
db_string = f"postgres+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}"
# db_string = f"postgres+psycopg2://{db_username}:{db_password}@{db_endpoint}"
engine = create_engine(db_string)
# Base.metadata.bind = engine
# conn = engine.connect()
"""
public access and security groups that allow outside connections
"""

db_session = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine
)
# scoped_session = scoped_session(db_session)


def get_session():
	return db_session()


def init_db():
	from src.database.models.models import Exercise, Muscle, Split, SplitTimeSeries, ExerciseTimeSeries
	Base.metadata.create_all(engine)


def destroy_tables():
	Base.metadata.drop_all(
		bind=engine
	)


def get_class_by_tablename(tablename):
	"""Return class reference mapped to table.

	:param tablename: String with name of table.
	:return: Class reference or None.
	"""
	print(list(Base._decl_class_registry.values()))
	for c in Base._decl_class_registry.values():
		if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
			return c


if __name__ == '__main__':
	init_db()
	destroy_tables()
	print(engine.table_names())

