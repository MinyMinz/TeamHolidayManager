from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from routes.auth import fetch_current_user
from models.user import Users as UsersModel
from models.holidayRequests import HolidayRequests as holidayModel
from schemas.holidayRequest import HolidayRequests as holidaySchema
from fastapi import APIRouter, status
from email.message import EmailMessage

import smtplib
import db.crud as crud
import numpy as np

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
    if holiday_request.approved and payload["role_name"] not in ["SuperAdmin", "Admin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to approve holiday requests"
        )
    crud.create(holidayModel, dict(holiday_request))

@holidayRouter.put("", status_code=status.HTTP_200_OK)
def update_holiday_request(holiday_request: holidaySchema, payload=Depends(fetch_current_user)):
    """Update an existing holiday request"""

    # Check if the user updating the holiday request is the same user or an admin or super admin
    if holiday_request.user_id != payload["id"] and payload["role_name"] not in ["SuperAdmin", "Admin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update a holiday request for another user"
        )

    if holiday_request.time_of_day not in ["AM", "PM"]:
    # If time of day is set then the number of days requested is half a day (0.5)
        number_of_request_days = 0.5
    else:
        # Calculate the number of days requested based on the start and end dates excluding weekends
        number_of_request_days = business_days_between_dates(holiday_request.start_date, holiday_request.end_date)

    # Check the user's remaining holidays against the number of days requested
    user = dict(crud.getOneRecordByColumnName(UsersModel, "id", holiday_request.user_id))
    if user["number_of_remaining_holidays"] < number_of_request_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have enough remaining holidays to make this request"
        )

    # Check that the holiday request exists
    holiday = crud.getOneRecordByColumnName(holidayModel, "id", holiday_request.id)

    # Check if holiday request approved field has changed
    if holiday["approved"] != holiday_request.approved:
        # Check if superAdmin or Admin has changed approved field to true and update the user's remaining holidays
        if not holiday["approved"] and holiday_request.approved:
            if payload["role_name"] in ["SuperAdmin", "Admin"]:
                try:
                    user["number_of_remaining_holidays"] = int(user["number_of_remaining_holidays"] - number_of_request_days)
                    send_calendar_invite(holiday_request, user)
                    crud.update(holidayModel, "id", dict(holiday_request))
                    crud.update(UsersModel, "id", user)
                    return {"message": "Calender invite sent successfully"}
                except Exception as error:
                    print(error)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="An error occurred while updating the holiday request: Internal Server error 500" 
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not authorized to approve holiday requests"
                )

    # Update the holiday request
    crud.update(holidayModel, "id", dict(holiday_request))
    return {"message": "Holiday request updated successfully"}

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

def business_days_between_dates(start_date, end_date):
    """Calculate the number of business days between two dates"""
    weekdays = np.busday_count(start_date, end_date)
    return weekdays

# When a holiday request is approved send an calendar invite to the user
def send_calendar_invite(holiday_request, user):
    # Convert date strings to datetime objects
    start_date = datetime.combine(holiday_request.start_date, datetime.min.time())
    end_date = datetime.combine(holiday_request.end_date, datetime.min.time())

    # Check if the holiday request is for a half day
    if hasattr(holiday_request, "time_of_day") and holiday_request.time_of_day:
        if holiday_request.time_of_day == "AM":
            start_date = start_date.replace(hour=9, minute=0)
            end_date = start_date.replace(hour=12, minute=30)
        elif holiday_request.time_of_day == "PM":
            start_date = start_date.replace(hour=13, minute=0)
            end_date = start_date.replace(hour=16, minute=30)
    else:
        # Set the start and end times for a full day
        start_date = start_date.replace(hour=9, minute=0)
        end_date = end_date.replace(hour=16, minute=30)

    # Create the email
    msg = EmailMessage()
    msg["From"] = "minhazrahman.baltic@gmail.com"
    msg["To"] = user["email"]
    msg["Subject"] = "Annual Leave Invitation"
    msg.set_content("Your annual leave request has been scheduled. Please find the calendar invite attached.")

    # Attach the ICS file
    ics_content = create_ics_event("Annual Leave", "Home", start_date, end_date, "Annual Leave", user["email"])

    msg.add_attachment(ics_content.encode("utf-8"), maintype="text", subtype="calendar", filename="AnnualLeave.ics")

    # Send the email via SMTP (Gmail)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("minhazrahman.baltic@gmail.com", "zows ebik qdqg gwbd")
        server.send_message(msg)

def create_ics_event(summary, location, start_time, end_time, description, uid):
    event = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Company//Your Application//EN
BEGIN:VEVENT
SUMMARY:{summary}
DTSTART:{start_time}
DTEND:{end_time}
LOCATION:{location}
DESCRIPTION:{description}
UID:{uid}
END:VEVENT
END:VCALENDAR""".format(
        summary=summary,
        start_time=start_time.strftime("%Y%m%dT%H%M%S"),
        end_time=end_time.strftime("%Y%m%dT%H%M%S"),
        location=location,
        description=description,
        uid=uid
    )
    return event