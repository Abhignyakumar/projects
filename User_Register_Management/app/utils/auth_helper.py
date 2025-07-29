from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from itsdangerous import URLSafeTimedSerializer, BadData
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status, Header

# Load environment variables from .env if present
load_dotenv()

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
FORGET_PASSWORD_SECRET = os.getenv("FORGET_PASSWORD_SECRET", "forget_secret")
PASSWORD_EXPIRY_DAYS = int(os.getenv("PASSWORD_EXPIRY_DAYS", 30))

# Password context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# JWT token decoding
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Forgot password token creation
def generate_reset_token(email: str) -> str:
    s = URLSafeTimedSerializer(FORGET_PASSWORD_SECRET)
    return s.dumps(email)

# Validate reset token
def validate_reset_token(token: str, max_age=86400):  # 24 hours
    s = URLSafeTimedSerializer(FORGET_PASSWORD_SECRET)
    try:
        return s.loads(token, max_age=max_age)
    except BadData:
        return None
#to destroy the JWT token
def destroy_jwt_token(token: str):
    # Optional: Add the token to a blacklist (e.g., Redis or MongoDB)
    print(f"Token destroyed or blacklisted: {token}")
    
    
async def get_current_user(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with Bearer",
        )
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: subject not found",
            )
        return {
            "user_id": user_id,
            "username": payload.get("username"),
            "email": payload.get("email")
        }
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token decoding error: {str(e)}"
        )