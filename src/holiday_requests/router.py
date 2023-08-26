from .models import HolidayRequests as holidayModel
from .schema import HolidayRequests as holidaySchema

import db.crud as crud

from fastapi import APIRouter, HTTPException, status

holidayRouter = APIRouter()

@holidayRouter.get("")
def fetch_all_holiday_requests():
    try:
        db_holiday = crud.dbGetAll(holidayModel)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No holiday requests found")
    return db_holiday

# Get all holiday requests for a specific user
@holidayRouter.get("/{user_id}")
def fetch_holiday_requests_by_user_id(user_id: int):
    try:
        db_holiday = crud.dbGet(holidayModel, 'user_id', user_id)
    except Exception:
        raise HTTPException(status_code= status.HTTP_200_OK, detail="No holiday requests found")
    return db_holiday

@holidayRouter.post("")
def create_holiday_request(holiday_request: holidaySchema):
    try:
        db_holiday_request = crud.dbCreate(holidayModel, holiday_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be created")
    return db_holiday_request

@holidayRouter.put("")
def update_holiday_request(holiday_request: holidaySchema):
    try:
        db_holiday_request = crud.dbUpdate(holidayModel, holiday_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be updated")
    return db_holiday_request

@holidayRouter.delete("/{holiday_id}")
def delete_holiday_request(holiday_id: int):
    try:
        crud.dbDelete(holidayModel, holiday_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="holiday request could not be deleted")
