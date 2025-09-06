from bson import ObjectId
from fastapi import HTTPException

#  Convert MongoDB ObjectId safely
def objectid_to_str(obj_id):
    return str(obj_id) if isinstance(obj_id, ObjectId) else obj_id

#  Validate ObjectId before using in DB queries
def validate_objectid(emp_id: str) -> ObjectId:
    try:
        return ObjectId(emp_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")

#  Standard response formatter
def response_formatter(success: bool, message: str, data=None):
    return {
        "success": success,
        "message": message,
        "data": data
    }
