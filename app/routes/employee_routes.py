# app/routes/employee_routes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from app.database import get_database
from app import crud
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeInDB,
)

router = APIRouter()


@router.post("/", response_model=EmployeeInDB, status_code=201)
async def create_employee(employee: EmployeeCreate, db=Depends(get_database)):
    return await crud.create_employee(db, employee.dict())


@router.get("/", response_model=List[EmployeeInDB])
async def list_employees(db=Depends(get_database)):
    return await crud.get_employees(db)


@router.get("/{employee_id}", response_model=EmployeeInDB)
async def get_employee(employee_id: str, db=Depends(get_database)):
    return await crud.get_employee_by_id(db, employee_id)


@router.put("/{employee_id}", response_model=EmployeeInDB)
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    db=Depends(get_database),
):
    return await crud.update_employee(db, employee_id, employee_update.dict())


@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee_id: str, db=Depends(get_database)):
    await crud.delete_employee(db, employee_id)
    return


# Search API: /employees/search?name=xxx
@router.get("/search/", response_model=List[EmployeeInDB])
async def search_employees(
    name: str = Query(..., description="Employee name to search"),
    db=Depends(get_database),
):
    return await crud.search_employees_by_name(db, name)


# Assign policy
@router.post("/{employee_id}/assign-policy/{policy_id}", response_model=EmployeeInDB)
async def assign_policy(
    employee_id: str,
    policy_id: str,
    db=Depends(get_database),
):
    return await crud.assign_policy_to_employee(db, employee_id, policy_id)
