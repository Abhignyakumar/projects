from fastapi import APIRouter, HTTPException, Depends, status, Header
from typing import Optional
from app.models.user_models import *
from app.services.user_service import *
from app.utils.logger import log_execution_time
from app.db.mongodb import user_collection
from app.utils.auth_helper import destroy_jwt_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# -------------------------- Register --------------------------
@router.post("/register")
@log_execution_time
async def register_user(data: RegisterUserRequest):
    await create_user(data.dict())
    return {"message": "User registered successfully"}

# -------------------------- Login --------------------------
@router.post("/login")
async def login_user(login_data: LoginRequest):
    user = await user_collection.find_one({
        "$or": [
            {"username": login_data.username},
            {"email": login_data.username},
            {"phone": login_data.username}
        ]
    })

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email/phone or password.")

    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email/phone or password.")

    token_data = {
        "sub": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------- Change Password --------------------------
@router.post("/change-password")
async def change_user_password(data: ChangePasswordRequest):
    await change_password(email=data.username, old_password=data.old_password, new_password=data.new_password)
    return {"message": "Password changed successfully."}

# -------------------------- Forgot Password --------------------------
@router.post("/forget-password")
async def forget_password(data: ForgotPasswordRequest):
    token = await forget_password_request(email=data.username)
    return {"message": "Reset link sent to your email", "token": token}

# -------------------------- Reset Password --------------------------
@router.post("/reset-password")
@log_execution_time
async def reset_password(data: ResetPasswordRequest):
    await reset_password_with_token(data.token, data.new_password)
    return {"message": "Password reset successfully"}

# -------------------------- Logout --------------------------
@router.post("/logout")
async def logout(authorization: str = Header(default=None)):
    try:
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            payload = decode_token(token)
            if payload and "username" in payload:
                logger.info(f"User {payload['username']} logged out.")
    except Exception as e:
        # Log it for debugging, but don't block the response
        logger.warning(f"Logout failed or token invalid: {str(e)}")

    return {"message": "User logged out successfully"}
