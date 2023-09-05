from pydantic import BaseModel, field_validator
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

    @field_validator("email", "password", "full_name", "team_name", "role_name")
    def fields_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("All fields must be non-empty strings")
        return v


class Auth(BaseModel):
    """Auth Schema"""

    email: str
    password: str

    class Config:
        from_attributes = True
