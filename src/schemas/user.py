from pydantic import BaseModel
from typing import Optional


class Users(BaseModel):
    """User Schema"""
    id: Optional[int]
    email: str
    password: str
    full_name: str
    team_name: str
    role_name: str

    class Config:
        from_attributes = True
    
    def __init__(self, email: str, password: str, full_name: str, team_name: str, role_name: str, id: Optional[int] = None):
        if not all([email, password, full_name, team_name, role_name]):
            raise ValueError("All fields must be non-empty strings")
        self.id = id
        self.email = email
        self.password = password
        self.full_name = full_name
        self.team_name = team_name
        self.role_name = role_name


class Auth(BaseModel):
    """Auth Schema"""
    email: str
    password: str

    class Config:
        from_attributes = True