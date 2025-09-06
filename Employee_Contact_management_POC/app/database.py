from pymongo import MongoClient
import certifi
from app.config import MONGO_URI, DB_NAME

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client[DB_NAME]
employee_collection = db["employees"]
