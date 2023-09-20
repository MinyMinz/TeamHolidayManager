from pydantic import BaseModel, field_validator


class Teams(BaseModel):
    """Team Schema
    \n Attributes:
        name (str): Team name
        description (str): Team description"""

    name: str
    description: str

    class Config:
        from_attributes = True

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name cannot be empty")
        return v
