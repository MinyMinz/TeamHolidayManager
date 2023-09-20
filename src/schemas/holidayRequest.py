from typing import Optional
from pydantic import BaseModel, FieldValidationInfo, field_validator
from datetime import date


class HolidayRequests(BaseModel):
    """Holiday Request Schema
    \n Attributes:
        id (int): The id of the holiday request
        description (str): The description of the holiday request
        start_date (date): The start date of the holiday request
        end_date (date): The end date of the holiday request
        time_of_day (str): The time of day of the holiday request
        team_name (str): The name of the team the holiday request is for
        user_id (int): The id of the user the holiday request is for
        approved (bool): Whether the holiday request has been approved or not"""

    id: Optional[int] = None
    description: Optional[str] = None
    start_date: date
    end_date: date
    time_of_day: Optional[str] = None
    team_name: str
    user_id: int
    approved: Optional[bool] = None

    class Config:
        from_attributes = True

    @field_validator("time_of_day")
    def validate_time_of_day(cls, value, info: FieldValidationInfo):
        """Validate that time_of_day is either "AM" or "PM" when start_date and end_date are equal"""
        start_date = info.data.get("start_date")
        end_date = info.data.get("end_date")
        if start_date == end_date:
            if value is None:
                raise ValueError(
                    "TimeOfDay is required when start_date and end_date are the same"
                )
            if value not in ["AM", "PM"]:
                raise ValueError("TimeOfDay must be either 'AM' or 'PM'.")
        else:
            if value is not None:
                raise ValueError(
                    "TimeOfDay must be null when start_date and end_date are not the same"
                )
        return value
