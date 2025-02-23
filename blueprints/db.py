import os
from dotenv import load_dotenv
import pymongo
from flask import flash, Blueprint

db_bp = Blueprint("db", __name__)

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING") # Get connection string from .env file

client=pymongo.MongoClient(connection_string) # Sets up database
db=client["Python_AI_Lab1"] # Name of database
users=db["users"] # Name of collection

# Method for finding user in db, placed in the db.py file because it's used by more than one blueprint
def get(user_name):
    user = users.find_one({"user name": user_name})  # Get user
    if user:
        username = user["user name"]  # Get user name
        password = user["password"]  # Get password
        return [username,password]
    else:
        flash("User not found")