# app/database.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "policy_manager_db")

_client = AsyncIOMotorClient(MONGO_URI)
_db = _client[MONGO_DB_NAME]


def get_database():
    """
    Dependency injection for MongoDB database.
    """
    return _db
