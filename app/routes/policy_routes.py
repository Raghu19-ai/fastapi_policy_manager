# app/routes/policy_routes.py
from typing import List
from fastapi import APIRouter, Depends

from app.database import get_database
from app import crud
from app.schemas import PolicyCreate, PolicyUpdate, PolicyInDB

router = APIRouter()


@router.post("/", response_model=PolicyInDB, status_code=201)
async def create_policy(policy: PolicyCreate, db=Depends(get_database)):
    return await crud.create_policy(db, policy.dict())


@router.get("/", response_model=List[PolicyInDB])
async def list_policies(db=Depends(get_database)):
    return await crud.get_policies(db)


@router.get("/{policy_id}", response_model=PolicyInDB)
async def get_policy(policy_id: str, db=Depends(get_database)):
    return await crud.get_policy_by_id(db, policy_id)


@router.put("/{policy_id}", response_model=PolicyInDB)
async def update_policy(
    policy_id: str,
    policy_update: PolicyUpdate,
    db=Depends(get_database),
):
    return await crud.update_policy(db, policy_id, policy_update.dict())


@router.delete("/{policy_id}", status_code=204)
async def delete_policy(policy_id: str, db=Depends(get_database)):
    await crud.delete_policy(db, policy_id)
    return
