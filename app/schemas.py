# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ---------- Employee Schemas ----------

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None


class EmployeeInDB(EmployeeBase):
    id: str
    assigned_policies: List[str] = []

    class Config:
        orm_mode = True


# ---------- Policy Schemas ----------

class PolicyBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    scalar_value: Optional[float] = None


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    scalar_value: Optional[float] = None


class PolicyInDB(PolicyBase):
    id: str

    class Config:
        orm_mode = True
