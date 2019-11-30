from flask import Blueprint
from flask_restful import Resource, Api
from src.database import get_session, Exercise as ExerciseDB, Day as DayDB, Muscle as MuscleDB
from pprint import pprint

sets_api_bp = Blueprint('sets_api', __name__)
sets_api = Api(sets_api_bp)


class Routine(Resource):
	def get(self):
		db_session = get_session()
		days = db_session.query(DayDB).all()
		routine = []
		for i, day in enumerate(days):
			routine.append({
				"id": day.id,
				"desc": day.desc,
				"muscles": []
			})
			muscles = db_session.query(MuscleDB).filter(
				MuscleDB.day_id == day.id
			).all()
			for muscle in muscles:
				excercises = db_session.query(ExerciseDB).filter(
					ExerciseDB.muscle_id == muscle.id
				).all()
				excercises_list = []
				for excercise in excercises:
					excercises_list.append({
						"id": excercise.id,
						"name": excercise.name,
						"sets": excercise.sets,
						"reps": excercise.reps,
						"weight": excercise.weight,
						"url": excercise.url,
						"muscleId": excercise.muscle_id
					})
				routine[i]["muscles"].append({
					"id": muscle.id,
					"name": muscle.name,
					"excercises": excercises_list
				})
		db_session.close()
		return routine


sets_api.add_resource(Routine, "/routine")

if __name__ == '__main__':
	test = Routine()
	pprint(test.get())
