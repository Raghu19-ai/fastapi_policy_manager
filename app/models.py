# app/models.py
from typing import List, Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom BSON ObjectId type for convenience.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# Collection names
EMPLOYEE_COLLECTION = "employees"
POLICY_COLLECTION = "policies"
