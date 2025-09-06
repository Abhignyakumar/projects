from fastapi import FastAPI
from app.routes import router as employee_router

app = FastAPI(title="Employee Contact Management System")

app.include_router(employee_router)

@app.get("/")
async def root():
    return{"message":"Employee Contact Management System"}