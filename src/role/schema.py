from pydantic import BaseModel, Field


class Roles(BaseModel):
    name: str = Field(...)
    description: str

    class Config:
        from_attributes = True
