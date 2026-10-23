from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

database = client["delivery_service"]
collection = database["orders"]
