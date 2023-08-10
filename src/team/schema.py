from typing import Union
from pydantic import BaseModel

class Roles(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class Teams(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class Users(BaseModel):
    email: str
    password: str
    full_name: str
    role_id: int
    team_id: int
    
    class Config:
        orm_mode = True