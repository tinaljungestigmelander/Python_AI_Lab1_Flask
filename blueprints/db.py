import os
from dotenv import load_dotenv
import pymongo
from flask import flash, Blueprint

db_bp = Blueprint("db", __name__)

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

client=pymongo.MongoClient(connection_string)
db=client["Python_AI_Lab1"]
users=db["users"]

def get(user_name):
    user = users.find_one({"user name": user_name})  # Hämta en användare
    if user:
        username = user["user name"]  # Hämta användarnamnet
        password = user["password"]  # Hämta lösenordet
        return [username,password]
    else:
        flash("User not found")