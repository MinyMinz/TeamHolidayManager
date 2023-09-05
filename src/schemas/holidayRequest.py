# from fastapi import HTTPException, status
from typing import Optional
from pydantic import BaseModel, FieldValidationInfo, field_validator
from datetime import date


class HolidayRequests(BaseModel):
    """Holiday Request Schema"""
    id: Optional[int] = None
    description: Optional[str] = None
    start_date: date
    end_date: date
    morning_or_afternoon: Optional[str] = None
    team_name: str
    user_id: int

    class Config:
        from_attributes = True
    
    def __init__(self, start_date: date, end_date: date, team_name: str, user_id: int):
        if not all([start_date, end_date, team_name, user_id]):
            raise ValueError("start_date, end_date, team_name, and user_id cannot be empty")
        self.start_date = start_date
        self.end_date = end_date
        self.team_name = team_name
        self.user_id = user_id

    @field_validator('start_date', 'end_date')
    def validate_dates(cls, v):
        """Validate that start_date is before end_date"""
        # Define the threshold date based on epoch date 01/01/1970
        threshold_date = date(1970, 1, 1)
        
        # Check if the input date is after the threshold date
        if v >= threshold_date:
            return v
        else:
            raise ValueError(f"Date {v} must be after {threshold_date}")    

    @field_validator("morning_or_afternoon")
    def validate_morning_or_afternoon(cls, v, info: FieldValidationInfo):
        """Validate that morning_or_afternoon is either "AM" or "PM" when start_date and end_date are equal"""
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
