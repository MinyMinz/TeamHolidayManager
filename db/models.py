import datetime as dt
from typing import Union
from pydantic import BaseModel

class Role(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None   
    class Config:
        orm_mode = True

class Team(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None

    class Config:
        orm_mode = True

class User(BaseModel):
    email: str
    password: str
    full_name: str
    role_id: int
    team_id: int
    class Config:
        orm_mode = True

class holidayRequests(BaseModel):
    id: int
    team_id: int
    user_id: int
    description: Union[str, None] = None
    start_date: dt.date
    end_date: dt.date
    morning: bool
    afternoon: bool
    class Config:
        orm_mode = True