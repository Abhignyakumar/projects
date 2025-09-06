from app.database import employee_collection
from bson import ObjectId

def employee_serializer(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "name": employee["name"],
        "email": employee["email"],
        "phone": employee["phone"],
        "department": employee.get("department"),
        "position": employee.get("position")
    }

# CREATE
def create_employee(employee: dict):
    result = employee_collection.insert_one(employee)
    return str(result.inserted_id)

# READ ALL
def get_all_employees():
    employees = employee_collection.find()
    return [employee_serializer(emp) for emp in employees]

# READ ONE
def get_employee(emp_id: str):
    employee = employee_collection.find_one({"_id": ObjectId(emp_id)})
    return employee_serializer(employee) if employee else None

# UPDATE
def update_employee(emp_id: str, data: dict):
    employee_collection.update_one({"_id": ObjectId(emp_id)}, {"$set": data})
    return get_employee(emp_id)

# DELETE
def delete_employee(emp_id: str):
    result = employee_collection.delete_one({"_id": ObjectId(emp_id)})
    return result.deleted_count > 0
