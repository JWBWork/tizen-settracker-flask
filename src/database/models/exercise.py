from sqlalchemy import Column, String, Integer
from src.database import Base


class Exercise(Base):
	__tablename__ = "exercises"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	sets = Column(Integer, nullable=False, default=4)
	reps = Column(Integer, nullable=False, default=8)
	weight = Column(Integer, nullable=True)
	muscle = Column(String, nullable=False)
	group = Column(String, nullable=False)

	def json(self):
		attr_dict = {k: v for k, v in self.__dict__.items() if k[0] != "_"}
		return attr_dict
