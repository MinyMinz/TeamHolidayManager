from pydantic import BaseModel, Field, validator
from typing import Optional


class Users(BaseModel):
    id: Optional[int]
    email: str = Field(...)
    password: str = Field(...)
    full_name: str = Field(...)
    team_name: str
    role_name: str

    class Config:
        from_attributes = True
