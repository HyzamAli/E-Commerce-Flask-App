from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("username", type = str, required = True, help = "username required")
	parser.add_argument("password", type = str, required = True, help = "password required")

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserModel.find_by_username(data["username"])
		if user:
			return {"Message" : "username already exists"}, 401

		user = UserModel(**data)
		try:
			user.save_to_db()
		except:
			return {"Message" : "Error Occured"}, 500
		return {"messsage" : "user creation successfull"}, 201