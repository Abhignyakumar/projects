from fastapi import FastAPI
from app.routes import auth

app = FastAPI(title="User Management System POC")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "OK", "message": "User Management API is running"}
