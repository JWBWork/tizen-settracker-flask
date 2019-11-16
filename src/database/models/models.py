from src.database import Base

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, \
	Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker
from src.database import engine, init_db


class Exercise(Base):
	__tablename__ = "Exercise"
	id = Column('id', Integer, primary_key=True)
	name = Column('name', Unicode)
	muscle_id = Column('muscle_id', Integer, ForeignKey('Muscle.id'))
	split_id = Column('split_id', Integer, ForeignKey('Split.id'))
	sets = Column('sets', Integer)
	reps = Column('reps', Integer)
	weight = Column('weight', Integer)

	split = relationship('Split', foreign_keys=split_id)
	muscle = relationship('Muscle', foreign_keys=muscle_id)


class Muscle(Base):
	__tablename__ = "Muscle"
	id = Column('id', Integer, primary_key=True)
	name = Column('name', Unicode)


class Split(Base):
	__tablename__ = "Split"
	id = Column('id', Integer, primary_key=True)
	name = Column('name', Unicode)


class SplitTimeSeries(Base):
	__tablename__ = "SplitTimeSeries"
	dt = Column('dt', DateTime, primary_key=True)
	split_id = Column('split_id', Integer, ForeignKey('Split.id'))

	split = relationship('Split', foreign_keys=split_id)


class ExerciseTimeSeries(Base):
	__tablename__ = "ExerciseTimeSeries"
	dt = Column('dt', DateTime, primary_key=True)
	exercise_id = Column('exercise_id', Integer, ForeignKey('Exercise.id'))
	weight = Column('weight', Integer)
	sets = Column('sets', Integer)
	reps = Column('reps', Integer)

	exercise = relationship('Exercise', foreign_keys=exercise_id)

