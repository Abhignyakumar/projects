from datetime import datetime, timedelta
from datetime import datetime, time, date
from bson import ObjectId
from app.db.mongodb import user_collection
from app.db.mongodb import mongodb
from app.utils.auth_helper import (
    hash_password, verify_password,
    create_access_token, generate_reset_token,
    validate_reset_token
)
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException, InvalidCredentialsException,
    PasswordExpiredException, PasswordReuseException,
    MaxResetRequestsException, TokenExpiredException
)

from passlib.context import CryptContext

async def is_duplicate_user(email: str, phone: str) -> bool:
    """Check if a user already exists with given email or phone."""
    existing_user = await mongodb.users.find_one({
        "$or": [{"email": email}, {"phone": phone}]
    })
    return existing_user is not None


def convert_date_to_datetime(data: dict):
    for key in ["dob", "doj"]:
        if key in data and isinstance(data[key], date):  # ✅ checks for datetime.date
            data[key] = datetime.combine(data[key], time.min)
    return data

async def create_user(user_data: dict):
    if await is_duplicate_user(user_data["email"], user_data["phone"]):
        raise UserAlreadyExistsException()

    user_data = convert_date_to_datetime(user_data)  # ✅ Convert date to datetime

    user_data["password"] = hash_password(user_data["password"])
    user_data["created_at"] = datetime.utcnow()
    user_data["password_changed_at"] = datetime.utcnow()
    user_data["reset_attempts"] = 0

    result = await mongodb.users.insert_one(user_data)
    return str(result.inserted_id)


async def validate_login(username: str, password: str):
    """Validate login credentials and check password expiration."""
    user = await mongodb.users.find_one({
        "$or": [{"email": username}, {"phone": username}]
    })

    if not user or not verify_password(password, user["password"]):
        raise InvalidCredentialsException()

    # Check if password expired (valid for 30 days)
    last_changed = user.get("password_changed_at")
    if last_changed and datetime.utcnow() - last_changed > timedelta(days=30):
        raise PasswordExpiredException()

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_collection = mongodb["users"]

async def change_password(email: str, old_password: str, new_password: str):
    user = await user_collection.find_one({"email": email})
    if not user:
        return False

    if not pwd_context.verify(old_password, user["password"]):
        return False

    hashed_new = pwd_context.hash(new_password)
    await user_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_new}}
    )
    return True

async def forget_password_request(email: str):
    """Initiate password reset. Generate and return token (max 3 attempts)."""
    user = await mongodb.users.find_one({"email": email})
    if not user:
        raise InvalidCredentialsException()

    if user.get("reset_attempts", 0) >= 3:
        raise MaxResetRequestsException()

    token = generate_reset_token(email)
    await mongodb.users.update_one(
        {"email": email},
        {"$inc": {"reset_attempts": 1}}
    )
    return token


async def reset_password_with_token(token: str, new_password: str):
    """Reset the password using a valid token and prevent reuse."""
    email = validate_reset_token(token)
    if not email:
        raise TokenExpiredException()

    user = await mongodb.users.find_one({"email": email})
    if not user:
        raise InvalidCredentialsException()

    if verify_password(new_password, user["password"]):
        raise PasswordReuseException()

    await mongodb.users.update_one(
        {"email": email},
        {"$set": {
            "password": hash_password(new_password),
            "password_changed_at": datetime.utcnow(),
            "reset_attempts": 0
        }}
    )
    return True
