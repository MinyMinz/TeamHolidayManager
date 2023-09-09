from typing import Optional
from pydantic import BaseModel, FieldValidationInfo, field_validator
from datetime import date


class HolidayRequests(BaseModel):
    """Holiday Request Schema"""

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
    def validate_fields(cls, value, info: FieldValidationInfo):
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")
        return value

    @field_validator("start_date", "end_date")
    def validate_dates(cls, value, info: FieldValidationInfo):
        """Validate that start_date is before end_date"""
        # Define the threshold date based on epoch date 01/01/1970
        threshold_date = date(1970, 1, 1)

        # Check if the input date is after the threshold date
        if info.field_name in ["start_date", "end_date"]:
            threshold_date = date(1970, 1, 1)
            if value < threshold_date:
                raise ValueError(f"{info.field_name} must be after {threshold_date}")
        return value

    @field_validator("time_of_day")
    def validate_time_of_day(cls, value, info: FieldValidationInfo):
        """Validate that time_of_day is either "AM" or "PM" when start_date and end_date are equal"""
        start_date = info.data.get("start_date")
        end_date = info.data.get("end_date")
        if start_date == end_date:
            if value is None:
                raise ValueError(
                    "Field is required when start_date and end_date are the same"
                )
            if value not in ["AM", "PM"]:
                raise ValueError("time of day must be either 'AM' or 'PM'.")
        else:
            if value is not None:
                raise ValueError(
                    "Field must be null when start_date and end_date are not the same"
                )
        return value
