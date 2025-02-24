from typing import Optional
from pydantic import BaseModel, FieldValidationInfo, field_validator
from datetime import date


class HolidayRequests(BaseModel):
    """Holiday Request Schema
    \n Attributes:
        id (int, Primary Key): Unique identifier for each holiday request.
        description (string, optional): Brief details about the holiday request.
        start_date (date): The date when the holiday starts.
        end_date (date): The date when the holiday ends.
        time_of_day (string, optional): Specific time of day for the holiday (e.g., morning, afternoon).
        team_name (string): The name of the team requesting the holiday.
        user_id (int, Foreign Key): Links the holiday request to a specific user in the system.
        approved (boolean, optional): Indicates if the holiday request has been approved."""

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

    @field_validator("team_name")
    def validate_team_name(cls, value, info: FieldValidationInfo):
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")
        return value

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
