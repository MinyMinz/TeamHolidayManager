from models.holidayRequests import HolidayRequests as holidayModel
from schemas.holidayRequest import HolidayRequests as holidaySchema

import db.crud as crud

from fastapi import APIRouter, status

holidayRouter = APIRouter()


@holidayRouter.get("/all")
def fetch_all_holiday_requests():
    """Fetch all holiday requests"""
    return crud.getAllRecords(holidayModel)


# Get all holiday requests for a specific user or team
@holidayRouter.get("")
def fetch_holiday_requests_by_user_or_team_name(
    user_id: int = None, team_name: str = None
):
    """Fetch all holiday requests for a specific user or team
    \n Args:
        user_id (int): The id of the user to fetch holiday requests for
        team_name (str): The name of the team to fetch holiday requests for"""
    if user_id is not None:
        return crud.getAllRecordsByColumnName(holidayModel, "user_id", user_id)
    elif team_name is not None:
        return crud.getAllRecordsByColumnName(holidayModel, "team_name", team_name)


@holidayRouter.post("")
def create_holiday_request(holiday_request: holidaySchema):
    """Create a new holiday request"""
    crud.create(holidayModel, dict(holiday_request))
    return status.HTTP_201_CREATED


@holidayRouter.put("")
def update_holiday_request(holiday_request: holidaySchema):
    """Update an existing holiday request"""
    crud.getOneRecordByColumnName(holidayModel, "id", holidaySchema.id)
    crud.update(holidayModel, "id", dict(holiday_request))
    return status.HTTP_202_ACCEPTED


@holidayRouter.delete("")
def delete_holiday_request(holiday_id: int):
    """Delete an existing holiday request
    \n Args:
        holiday_id (int): The id of the holiday request to delete"""
    crud.delete(holidayModel, holiday_id)
    return status.HTTP_202_ACCEPTED
