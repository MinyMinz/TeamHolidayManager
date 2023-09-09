from models.holidayRequests import HolidayRequests as holidayModel
from schemas.holidayRequest import HolidayRequests as holidaySchema

import db.crud as crud

from fastapi import APIRouter, status

holidayRouter = APIRouter()


# Get all holiday requests for and optionally specify a user or team
@holidayRouter.get("", status_code=status.HTTP_200_OK)
def fetch_holiday_requests(user_id: int = None, team_name: str = None):
    """Fetch all holiday requests for a specific user or team
    \n Args:
        user_id (int): The id of the user to fetch holiday requests for
        team_name (str): The name of the team to fetch holiday requests for"""
    if user_id is not None:
        return crud.getAllRecordsByColumnName(holidayModel, "user_id", user_id, "id")
    elif team_name is not None:
        return crud.getAllRecordsByColumnName(holidayModel, "team_name", team_name, "id")
    else:
        return crud.getAllRecords(holidayModel, "id")


@holidayRouter.post("", status_code=status.HTTP_201_CREATED)
def create_holiday_request(holiday_request: holidaySchema):
    """Create a new holiday request"""
    crud.create(holidayModel, dict(holiday_request))


@holidayRouter.put("", status_code=status.HTTP_200_OK)
def update_holiday_request(holiday_request: holidaySchema):
    """Update an existing holiday request"""
    crud.getOneRecordByColumnName(holidayModel, "id", holiday_request.id)
    crud.update(holidayModel, "id", dict(holiday_request))


@holidayRouter.delete("", status_code=status.HTTP_200_OK)
def delete_holiday_request(holiday_id: int):
    """Delete an existing holiday request
    \n Args:
        holiday_id (int): The id of the holiday request to delete"""
    crud.getOneRecordByColumnName(holidayModel, "id", holiday_id)
    crud.delete(holidayModel, holiday_id)
