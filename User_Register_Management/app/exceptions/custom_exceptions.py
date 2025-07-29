from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists with this email or phone number.")

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid email/phone or password.")

class PasswordReuseException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="New password cannot be same as previous password.")

class PasswordExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Password expired. Please reset your password.")

class MaxResetRequestsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail="Maximum reset password requests reached. Try later.")

class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Reset token expired or invalid.")
