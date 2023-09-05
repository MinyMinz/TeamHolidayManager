from db.database import Base
from sqlalchemy import String, Column


class Teams(Base):
    """Team Model"""
    __tablename__ = "Teams"

    name = Column(String(50), primary_key=True, unique=True)
    description = Column(String(100), nullable=True)
