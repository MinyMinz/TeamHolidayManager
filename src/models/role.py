from db.database import Base
from sqlalchemy import String, Column


class Roles(Base):
    """Role Model"""
    __tablename__ = "Roles"

    name = Column(String(50), primary_key=True, unique=True)
    description = Column(String(100), nullable=True)
