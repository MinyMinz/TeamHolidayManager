from pydantic import BaseModel, field_validator


class Roles(BaseModel):
    """Role Schema
    \n Attributes:
        name (str): Role name
        description (str): Role description"""

    name: str
    description: str

    class Config:
        from_attributes = True

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name cannot be empty")
        return v
