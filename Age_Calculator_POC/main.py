from fastapi import FastAPI
from schemas import DOBInput
import utils

app = FastAPI(title="Age Calculator API", version="1.0")

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "Age Calculator API is running"}

@app.post("/age", tags=["Age"])
def get_age(data: DOBInput):
    delta = utils.calculate_age(data.date_of_birth)
    return {"years": delta.years, "months": delta.months, "days": delta.days}

@app.post("/age/months ", tags=["Age"])
def get_age_in_months(data: DOBInput):
    return {"age_in_months": utils.age_in_months(data.date_of_birth)}

@app.post("/age/days", tags=["Age"])
def get_age_in_days(data: DOBInput):
    return {"age_in_days": utils.age_in_days(data.date_of_birth)}

@app.post("/age/weeks", tags=["Age"])
def get_age_in_weeks(data: DOBInput):
    return {"age_in_weeks": utils.age_in_weeks(data.date_of_birth)}

@app.post("/age/hours", tags=["Age"])
def get_age_in_hours(data: DOBInput):
    return {"age_in_hours": utils.age_in_hours(data.date_of_birth)}

@app.post("/age/minutes", tags=["Age"])
def get_age_in_minutes(data: DOBInput):
    return {"age_in_minutes": utils.age_in_minutes(data.date_of_birth)}

@app.post("/next-birthday", tags=["Birthday"])
def days_to_next_birthday(data: DOBInput):
    return {"days_until_next_birthday": utils.time_until_next_birthday(data.date_of_birth)}
