from fastapi import APIRouter, HTTPException
from app.models import Employee, UpdateEmployee
from app import crud

router = APIRouter()

@router.post("/employees")
def create(employee: Employee):
    emp_id = crud.create_employee(employee.dict())
    return {"message": "Employee created successfully", "id": emp_id}

@router.get("/employees")
def get_all():
    return crud.get_all_employees()

@router.get("/employees/{emp_id}")
def get_one(emp_id: str):
    employee = crud.get_employee(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{emp_id}")
def update(emp_id: str, employee: UpdateEmployee):
    updated = crud.update_employee(emp_id, {k: v for k, v in employee.dict().items() if v is not None})
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully", "employee": updated}

@router.delete("/employees/{emp_id}")
def delete(emp_id: str):
    success = crud.delete_employee(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
