# app/crud.py
from typing import List, Optional

from bson import ObjectId
from fastapi import HTTPException, status

from app.models import EMPLOYEE_COLLECTION, POLICY_COLLECTION
from app.utils.logger import logger


# --------- Helper ----------

def _serialize_doc(doc) -> dict:
    if not doc:
        return doc
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc


# --------- Employee CRUD ----------

async def create_employee(db, employee_data: dict) -> dict:
    existing = await db[EMPLOYEE_COLLECTION].find_one({"email": employee_data["email"]})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists",
        )

    employee_data["assigned_policies"] = []
    result = await db[EMPLOYEE_COLLECTION].insert_one(employee_data)
    new_employee = await db[EMPLOYEE_COLLECTION].find_one({"_id": result.inserted_id})
    logger.info(f"Created employee with id {result.inserted_id}")
    return _serialize_doc(new_employee)


async def get_employee_by_id(db, employee_id: str) -> dict:
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee id")

    employee = await db[EMPLOYEE_COLLECTION].find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return _serialize_doc(employee)


async def get_employees(db) -> List[dict]:
    cursor = db[EMPLOYEE_COLLECTION].find()
    employees = [ _serialize_doc(doc) async for doc in cursor ]
    return employees


async def update_employee(db, employee_id: str, update_data: dict) -> dict:
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee id")

    update_data = {k: v for k, v in update_data.items() if v is not None}
    result = await db[EMPLOYEE_COLLECTION].update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": update_data},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated = await db[EMPLOYEE_COLLECTION].find_one({"_id": ObjectId(employee_id)})
    logger.info(f"Updated employee {employee_id}")
    return _serialize_doc(updated)


async def delete_employee(db, employee_id: str) -> None:
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee id")

    result = await db[EMPLOYEE_COLLECTION].delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    logger.info(f"Deleted employee {employee_id}")


async def search_employees_by_name(db, name: str) -> List[dict]:
    cursor = db[EMPLOYEE_COLLECTION].find({"name": {"$regex": name, "$options": "i"}})
    employees = [_serialize_doc(doc) async for doc in cursor]
    return employees


# --------- Policy CRUD ----------

async def create_policy(db, policy_data: dict) -> dict:
    result = await db[POLICY_COLLECTION].insert_one(policy_data)
    new_policy = await db[POLICY_COLLECTION].find_one({"_id": result.inserted_id})
    logger.info(f"Created policy {result.inserted_id}")
    return _serialize_doc(new_policy)


async def get_policy_by_id(db, policy_id: str) -> dict:
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=400, detail="Invalid policy id")

    policy = await db[POLICY_COLLECTION].find_one({"_id": ObjectId(policy_id)})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return _serialize_doc(policy)


async def get_policies(db) -> List[dict]:
    cursor = db[POLICY_COLLECTION].find()
    policies = [_serialize_doc(doc) async for doc in cursor]
    return policies


async def update_policy(db, policy_id: str, update_data: dict) -> dict:
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=400, detail="Invalid policy id")

    update_data = {k: v for k, v in update_data.items() if v is not None}
    result = await db[POLICY_COLLECTION].update_one(
        {"_id": ObjectId(policy_id)},
        {"$set": update_data},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Policy not found")

    updated = await db[POLICY_COLLECTION].find_one({"_id": ObjectId(policy_id)})
    logger.info(f"Updated policy {policy_id}")
    return _serialize_doc(updated)


async def delete_policy(db, policy_id: str) -> None:
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=400, detail="Invalid policy id")

    result = await db[POLICY_COLLECTION].delete_one({"_id": ObjectId(policy_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Policy not found")
    logger.info(f"Deleted policy {policy_id}")


# --------- Assign Policy to Employee ----------

async def assign_policy_to_employee(db, employee_id: str, policy_id: str) -> dict:
    # Validate employee
    employee = await get_employee_by_id(db, employee_id)

    # Validate policy
    await get_policy_by_id(db, policy_id)

    # Prevent duplicates
    if policy_id in employee.get("assigned_policies", []):
        raise HTTPException(
            status_code=400,
            detail="Policy already assigned to this employee",
        )

    await db[EMPLOYEE_COLLECTION].update_one(
        {"_id": ObjectId(employee_id)},
        {"$addToSet": {"assigned_policies": policy_id}},
    )

    updated = await get_employee_by_id(db, employee_id)
    logger.info(f"Assigned policy {policy_id} to employee {employee_id}")
    return updated
