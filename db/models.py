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

class teamCalendar(BaseModel):
    id: int
    team_id: int
    user_id: int
    name: str
    description: Union[str, None] = None
    start_date: str
    end_date: str
    class Config:
        orm_mode = True