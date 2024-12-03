from pydantic import BaseModel, FieldValidationInfo, field_validator
from typing import Optional


class Users(BaseModel):
    """User Schema
    \n Attributes:
        id (int): User id
        email (str): User email
        password (str): User password
        full_name (str): User full name
        team_name (str): User team name
        role_name (str): User role name"""

    id: Optional[int]
    email: str
    password: str
    full_name: str
    team_name: str
    role_name: str

    class Config:
        from_attributes = True

    @field_validator("email", "password", "full_name", "team_name", "role_name")
    def fields_must_not_be_empty(cls, v, info: FieldValidationInfo):
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v