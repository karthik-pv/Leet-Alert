from pymongo import MongoClient
import os
from dotenv import load_dotenv


def connectToDatabase():
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["LeetAlert"]
    return db
