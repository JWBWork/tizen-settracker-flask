import pygsheets
from os import path
from src.database import init_db, get_session, Exercise

key_path = path.join(path.dirname(__file__), "google_key.json")
gs_client = pygsheets.authorize(service_account_file=key_path)

print(gs_client.spreadsheet_titles())
sets_sheet = gs_client.open("SetsApp")
ex_wksheet = sets_sheet.worksheet_by_title("Exercises")

exercises_df = ex_wksheet.get_as_df()
# print(exercises_df)
init_db()
db_session = get_session()

for i, exercise in exercises_df.iterrows():
	db_ex = Exercise(
		name=exercise['Name'],
		muscle=exercise['Muscle'],
		group=exercise['Group']
	)
	db_session.add(db_ex)
db_session.commit()
