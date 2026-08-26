from pymongo import MongoClient
from config import DATABASE_NAME, MONGO_URI


client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]

users = database["users"]
rooms = database["rooms"]