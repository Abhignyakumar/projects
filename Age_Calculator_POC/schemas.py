from pydantic import BaseModel
from datetime import date

class DOBInput(BaseModel):
    date_of_birth: date
