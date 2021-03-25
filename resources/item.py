from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price", type = float, required=True, help="price required")
	parser.add_argument("store_id", type = int, required=True, help="store required")

	def post(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return {"Message" : "Item already exists"}, 401
		request_data = Item.parser.parse_args()
		item = ItemModel(name, request_data["price"], request_data["store_id"])
		try:
			item.save_to_db()
		except:
			return {"Message" : "Unexpected Error occured"}, 500
		return item.json(), 201

	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item is None:
			return {"Message" : "Item not found"}, 404
		return item.json()

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item is None:
			return {"Message" : "Item {} not found".format(name)}, 401
		try:
			item.delete_from_db()
		except:
			return {"Message" : "Unexpected Error occured"}, 500
		return {"Message" : "Item {} deleted".format(name)}

	def put(self, name):
		request_data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		if item is None:
			item = ItemModel(name, request_data["price"], request_data["store_id"])
		else:
			item.price = request_data["price"]
			item.store_id = request_data["store_id"]
		try:
			item.save_to_db()
		except:
			return {"Message" : "Unexpected Error occured"}, 500
		return item.json()


class ItemList(Resource):
	@jwt_required()
	def get(self):
		return {"items" : [item.json() for item in ItemModel.query.all()]}
