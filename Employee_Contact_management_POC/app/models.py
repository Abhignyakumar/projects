from pydantic import BaseModel, EmailStr
from typing import Optional

class Employee(BaseModel):
    name: str
    email: EmailStr
    phone: str
    department: Optional[str] = None
    position: Optional[str] = None

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
