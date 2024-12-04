from fastapi import APIRouter, Depends, status, HTTPException
from routes.auth import fetch_current_user
from models.holidayRequests import HolidayRequests as holidayModel
from schemas.holidayRequest import HolidayRequests as holidaySchema
import db.crud as crud
from fastapi import APIRouter, status

holidayRouter = APIRouter()

# Get all holiday requests for and optionally specify a user or team
@holidayRouter.get("", status_code=status.HTTP_200_OK)
def fetch_holiday_requests(payload=Depends(fetch_current_user)):
    """Fetch all holiday requests for a specific user or team
    \n Args:
        user_id (int): The id of the user to fetch holiday requests for
        team_name (str): The name of the team to fetch holiday requests for"""
    if payload["role_name"] == "User":
        return crud.getHolidayRequestsByField("user_id", payload["id"], "id")
    elif payload["role_name"] == "Admin":
        return crud.getHolidayRequestsByField("team_name", payload["team_name"], "id")
    else:
        return crud.getAllHolidayRequests("id")

@holidayRouter.post("", status_code=status.HTTP_201_CREATED)
def create_holiday_request(holiday_request: holidaySchema, payload=Depends(fetch_current_user)):
    """Create a new holiday request"""
    #Check if user creating the holiday request is the same user
    if holiday_request.user_id != payload["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create a holiday request for another user"
        )
    crud.create(holidayModel, dict(holiday_request))

@holidayRouter.put("", status_code=status.HTTP_200_OK)
def update_holiday_request(holiday_request: holidaySchema, payload=Depends(fetch_current_user)):
    """Update an existing holiday request"""

    # Check if the user updating the holiday request is the same user or an admin or super admin
    if holiday_request.user_id != payload["id"] and payload["role_name"] != "SuperAdmin" and payload["role_name"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update a holiday request for another user"
        )
    # First check that the holiday request exists then update it
    crud.getOneRecordByColumnName(holidayModel, "id", holiday_request.id)
    crud.update(holidayModel, "id", dict(holiday_request))

@holidayRouter.delete("", status_code=status.HTTP_200_OK)
def delete_holiday_request(holiday_id: int, payload=Depends(fetch_current_user)):
    """Delete an existing holiday request
    \n Args:
        holiday_id (int): The id of the holiday request to delete"""
    # first check that the holiday request exists then delete it
    existingHoliday = crud.getOneRecordByColumnName(holidayModel, "id", holiday_id)
    if existingHoliday["user_id"] != payload["id"] and payload["role_name"] != "SuperAdmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete a holiday request for another user"
        )

    crud.delete(holidayModel, "id", holiday_id)
