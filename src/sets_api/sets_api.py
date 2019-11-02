from flask import Blueprint
from flask_restful import Resource, Api
from src.database import Exercise as ExerciseDB, get_session

sets_api_bp = Blueprint('sets_api', __name__)
sets_api = Api(sets_api_bp)


class Exercises(Resource):
	def get(self):
		db_session = get_session()
		exercises = db_session.query(ExerciseDB).all()
		exercises = [e.json() for e in exercises]
		db_session.close()
		return exercises


sets_api.add_resource(Exercises, "/exercises")

if __name__ == '__main__':
	test = Exercises()
	print(test.get())
