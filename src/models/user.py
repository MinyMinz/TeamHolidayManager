from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship


class Users(Base):
    """User Model"""
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    team_name = Column(String, ForeignKey("Teams.name"))
    role_name = Column(String, ForeignKey("Roles.name"))
    number_of_allocated_holdiays = Column(Integer, nullable=False)
    number_of_remaining_holidays = Column(Integer, nullable=False)

    teamFK = relationship("Teams")
    roleFK = relationship("Roles")
