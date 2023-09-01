from .models import HolidayRequests as holidayModel
from .schema import HolidayRequests as holidaySchema

import db.crud as crud

from fastapi import APIRouter, HTTPException, status

holidayRouter = APIRouter()


@holidayRouter.get("/all")
def fetch_all_holiday_requests():
    try:
        db_holiday = crud.dbGetAllRecords(holidayModel)
        if db_holiday is None or len(db_holiday) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No holiday requests found")
    except Exception:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No holiday requests found")
    return db_holiday


# Get all holiday requests for a specific user or team
@holidayRouter.get("")
def fetch_holiday_requests_by_user_or_team_name(
    user_id: int = None, team_name: str = None
):
    if user_id is not None:
        try:
            db_holiday = crud.dbGetAllRecordsByColumnName(
                holidayModel, "user_id", user_id
            )
        except Exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No holiday requests found")
    elif team_name is not None:
        try:
            db_holiday = crud.dbGetAllRecordsByColumnName(
                holidayModel, "team_name", team_name
            )
        except Exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No holiday requests found")
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid request")
    return db_holiday


@holidayRouter.post("")
def create_holiday_request(holiday_request: holidaySchema):
    try:
        crud.dbCreate(holidayModel, dict(holiday_request))
    except HTTPException:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "holiday request could not be created"
        )
    return "Create successfull"


@holidayRouter.put("")
def update_holiday_request(holiday_request: holidaySchema):
    try:
        db_holiday = crud.dbGetOneRecordByColumnName(
            holidayModel, "id", holidaySchema.id
        )
        if db_holiday is None:
            raise HTTPException
    except Exception:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Cannot update. Holiday request with id: {holiday_request.id} does not exist",
        )
    try:
        crud.dbUpdate(holidayModel, "id", dict(holiday_request))
    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "holiday request could not be updated"
        )
    return "Update successfull"


@holidayRouter.delete("/{holiday_id}")
def delete_holiday_request(holiday_id: int):
    try:
        crud.dbDelete(holidayModel, holiday_id)
    except Exception:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, "holiday request could not be deleted"
        )
    return "Deleted successfully"
