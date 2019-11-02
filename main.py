from flask import Flask
from src import sets_api_bp
from src.database import init_db

init_db()
app = Flask(__name__)
app.register_blueprint(sets_api_bp)

if __name__ == '__main__':
	init_db()
	app.run()
