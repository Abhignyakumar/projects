# app/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
mongodb = client["user_management"]

# Define the user collection (you can define more collections here)
user_collection = mongodb["users"]
