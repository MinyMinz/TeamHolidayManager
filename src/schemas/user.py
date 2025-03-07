from pydantic import BaseModel, FieldValidationInfo, field_validator
from typing import Optional

#Used for creation of a user
class Users(BaseModel):
    """User Schema
    \n Attributes:
        email (str): User email
        password (str): User password
        full_name (str): User full name
        team_name (str): User team name
        role_name (str): User role name
        number_of_allocated_holdiays (int): User allocated holidays
        number_of_remaining_holidays (int): User remaining 
        """

    email: str
    password: str
    full_name: str
    team_name: str
    role_name: str
    allocated_holidays: int
    remaining_holidays: int

    class Config:
        from_attributes = True

    @field_validator("email", "password", "full_name", "team_name", "role_name")
    def fields_must_not_be_empty(cls, v, info: FieldValidationInfo):
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v

#Use for Viewing and updating a user
class UserAPI(BaseModel):
    """UserAPI Schema
    \n Attributes:
        id (int): User id
        email (str): User email
        full_name (str): User full name
        team_name (str): User team name
        role_name (str): User role name
        allocated_holidays (int): User allocated holidays
        remaining_holidays (int): User remaining holidays"""

    id: Optional[int]
    email: str
    full_name: str
    team_name: str
    role_name: str
    allocated_holidays: Optional[int]
    remaining_holidays: Optional[int]

    @field_validator("email", "full_name", "team_name", "role_name")
    def fields_must_not_be_empty(cls, v, info: FieldValidationInfo):
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v
    
#Used for authentication
class UserAuthAPI(BaseModel):
    """UserAPI Schema
    \n Attributes:
        id (int): User id
        email (str): User email
        full_name (str): User full name
        team_name (str): User team name
        role_name (str): User role name"""

    id: Optional[int]
    email: str
    full_name: str
    team_name: str
    role_name: str

    @field_validator("email", "full_name", "team_name", "role_name")
    def fields_must_not_be_empty(cls, v, info: FieldValidationInfo):
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v