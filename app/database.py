from pymongo import MongoClient
from os import getenv


def db_connect():
    uri = getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    database = client["delivery_service"]
    return database["orders"]


def db_logs_connect():
    uri = getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    database = client["delivery_service"]
    return database["logs"]
