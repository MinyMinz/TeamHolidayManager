from pydantic import BaseModel


class Roles(BaseModel):
    """Role Schema"""
    name: str
    description: str

    class Config:
        from_attributes = True

    def __init__(self, name: str):
        if not all([name]):
            raise ValueError("Name cannot be empty")
        self.name = name