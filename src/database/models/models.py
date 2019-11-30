from src.database import Base

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, \
	Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker


class Exercise(Base):
	__tablename__ = "Exercise"
	id = Column('id', Integer, primary_key=True)
	name = Column('name', Unicode, unique=True)
	sets = Column('sets', Integer, default=4)
	reps = Column('reps', Integer, default=8)
	weight = Column('weight', Integer, nullable=True)
	url = Column('url', String, nullable=False)
	muscle_id = Column('muscle_id', Integer, ForeignKey('Muscle.id'))

	muscle = relationship('Muscle', foreign_keys=muscle_id)


class Muscle(Base):
	__tablename__ = "Muscle"
	id = Column('id', Integer, primary_key=True)
	name = Column('name', Unicode, unique=True)
	day_id = Column(Integer, ForeignKey('Day.id'))

	day = relationship('Day', back_populates="muscles")


class Day(Base):
	__tablename__ = "Day"
	id = Column('id', Integer, primary_key=True)
	desc = Column('name', Unicode, unique=True)
	muscles = relationship('Muscle', back_populates="day")


class DayTimeSeries(Base):
	__tablename__ = "DayTimeSeries"
	dt = Column('dt', DateTime, primary_key=True)
	day_id = Column(Integer, ForeignKey('Day.id'))

	day = relationship('Day', foreign_keys=day_id)


class ExerciseTimeSeries(Base):
	__tablename__ = "ExerciseTimeSeries"
	dt = Column('dt', DateTime, primary_key=True)
	weight = Column('weight', Integer)
	sets = Column('sets', Integer)
	reps = Column('reps', Integer)
	exercise_id = Column(Integer, ForeignKey('Exercise.id'))

	exercise = relationship('Exercise', foreign_keys=exercise_id)


