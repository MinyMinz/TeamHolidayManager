import datetime as dt
from typing import Union
from pydantic import BaseModel

class holidayRequests(BaseModel):
    id: int
    team_id: int
    user_id: int
    description: Union[str, None] = None
    start_date: dt.date
    end_date: dt.date
    morning_or_afternoon: bool

    class Config:
        orm_mode = True