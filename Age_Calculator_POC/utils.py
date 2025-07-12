from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_age(dob: date):
    today = date.today()
    return relativedelta(today, dob)

def age_in_days(dob: date):
    return (date.today() - dob).days

def age_in_weeks(dob: date):
    return age_in_days(dob) // 7

def age_in_hours(dob: date):
    return age_in_days(dob) * 24

def age_in_minutes(dob: date):
    return age_in_hours(dob) * 60

def age_in_months(dob: date):
    delta = calculate_age(dob)
    return delta.years * 12 + delta.months

def time_until_next_birthday(dob: date):
    today = date.today()
    next_birthday = dob.replace(year=today.year)

    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    return (next_birthday - today).days
