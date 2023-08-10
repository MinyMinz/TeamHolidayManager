from .models import HolidayRequests as holiday_model
from .schema import HolidayRequests as holiday_schema

import db.crud as crud

from fastapi import APIRouter, HTTPException, status

holidayRouter = APIRouter()

@holidayRouter.get("")
def fetch_all_holiday_requests():
    try:
        db_holiday = crud.dbGetAll(holiday_model)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No holiday requests found")
    return db_holiday

# Get all holiday requests for a specific user
@holidayRouter.get("/{user_id}")
def fetch_holiday_requests_by_user_id(user_id: int):
    try:
        db_holiday = crud.dbGet(holiday_model, 'user_id', user_id)
    except Exception:
        raise HTTPException(status_code= status.HTTP_200_OK, detail="No holiday requests found")
    return db_holiday

@holidayRouter.post("")
def create_holiday_request(holiday_request: holiday_schema):
    try:
        db_holiday_request = crud.dbCreate(holiday_model, holiday_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be created")
    return db_holiday_request

@holidayRouter.put("")
def update_holiday_request(holiday_request: holiday_schema):
    try:
        db_holiday_request = crud.dbUpdate(holiday_model, holiday_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be updated")
    return db_holiday_request

@holidayRouter.delete("/{holiday_id}")
def delete_holiday_request(holiday_id: int):
    try:
        crud.dbDelete(holiday_model, holiday_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be deleted")
