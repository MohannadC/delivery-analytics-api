from pymongo import MongoClient


def db_connect():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    database = client["delivery_service"]
    return database["orders"]


def db_logs_connect():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    database = client["delivery_service"]
    return database["logs"]
