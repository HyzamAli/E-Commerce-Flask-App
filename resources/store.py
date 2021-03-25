from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store is None:
			return {"Message" : "Store does not exists"}, 401
		return store.json()

	def post(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return {"Message" : "Store already exists"}, 401
		try:
			store = StoreModel(name)
			store.save_to_db()
		except:
			return {"Message" : "Internal Server Error"}, 500
		return store.json(), 201
		
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store is None:
			return {"Message" : "Store does not exists"}, 401
		try:
			store = StoreModel(name)
			store.delete_from_db()
		except:
			return {"Message" : "Internal Server Error"}, 500
		return {"Message"  : "Successfully deleted"}	


class StoreList(Resource):
	def get(self):
		return {"stores" : [store.json() for store in StoreModel.query.all()]}