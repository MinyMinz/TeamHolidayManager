# from fastapi import HTTPException, status
from typing import Optional
from pydantic import BaseModel, FieldValidationInfo, Field, field_validator
from datetime import date


class HolidayRequests(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    start_date: date
    end_date: date
    morning_or_afternoon: Optional[str] = None
    team_name: str
    user_id: int

    class Config:
        from_attributes = True

    @field_validator('start_date', 'end_date')
    def validate_dates(cls, v):
        # Define the threshold date based on epoch date 01/01/1970
        threshold_date = date(1970, 1, 1)
        
        # Check if the input date is after the threshold date
        if v >= threshold_date:
            return v
        else:
            raise ValueError(f"Date {v} must be after {threshold_date}")    

    # Validate that morning_or_afternoon is either "AM" or "PM" when start_date and end_date are equal
    @field_validator("morning_or_afternoon")
    def validate_morning_or_afternoon(cls, v, info: FieldValidationInfo):
        start_date = info.data.get("start_date")
        end_date = info.data.get("end_date")
        if start_date == end_date:
            if v is None:
                raise ValueError(
                    "morning_or_afternoon is required when start_date and end_date are equal"
                )
            if v not in ["AM", "PM"]:
                raise ValueError(
                    'morning_or_afternoon must be either "AM" or "PM" when start_date and end_date are equal'
                )
        else:
            if v is not None:
                raise ValueError(
                    "morning_or_afternoon must be null when start_date and end_date are not equal"
                )
        return v
