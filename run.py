from db import db
from app import app

db.init_app(app)

@app.before_first_request
def create_Tables():
	db.create_all()