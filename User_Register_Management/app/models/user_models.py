from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import date

class RegisterUserRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=5)
    email: EmailStr
    phone: constr(strip_whitespace=True, min_length=10, max_length=10)
    password: constr(min_length=8, max_length=20)
    first_name: str
    last_name: str
    dob: date
    doj: date
    address: str
    comment: Optional[str]
    active: bool = True

class LoginRequest(BaseModel):
    username: str  # Email or Phone
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChangePasswordRequest(BaseModel):
    username: str  # instead of email
    old_password: str
    new_password: str


class ForgotPasswordRequest(BaseModel):
    username: str  # Email or Phone

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class GenericResponse(BaseModel):
    message: str
