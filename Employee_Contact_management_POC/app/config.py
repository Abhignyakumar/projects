import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://akmudumbai:5xoOh4i261MnkmFa@myprojects.ylji0m2.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "employee_db")
