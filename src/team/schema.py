from pydantic import BaseModel, Field


class Teams(BaseModel):
    name: str = Field(...)
    description: str

    class Config:
        from_attributes = True
