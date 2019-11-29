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
			# print(day.desc)
			routine.append({
				"id": day.id,
				"desc": day.desc,
				"muscles": []
			})
			muscles = db_session.query(MuscleDB).filter(
				MuscleDB.day_id == day.id
			).all()
			for muscle in muscles:
				# print(f"\t{muscle.name}")
				# routine[i][muscle.name] = []
				# routine[i]["muscles"] = []
				excercises = db_session.query(ExerciseDB).filter(
					ExerciseDB.muscle_id == muscle.id
				).all()
				excercises_list = []
				for excercise in excercises:
					# print(f"\t\t{excercise.name}")
					# routine[i][muscle.name].append({
					# 	"name": excercise.name,
					# 	"sets": excercise.sets,
					# 	"reps": excercise.reps,
					# 	"weight": excercise.weight,
					# 	"muscle": muscle.name
					# })
					excercises_list.append({
						"name": excercise.name,
						"sets": excercise.sets,
						"reps": excercise.reps,
						"weight": excercise.weight
					})
				routine[i]["muscles"].append({
					"name": muscle.name,
					"excercises": excercises_list
				})
		return routine


sets_api.add_resource(Routine, "/routine")

if __name__ == '__main__':
	test = Routine()
	pprint(test.get())
