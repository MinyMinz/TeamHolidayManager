from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    team_name = Column(Integer, ForeignKey("Teams.name"))
    role_name = Column(Integer, ForeignKey("Roles.name"))

    teamFK = relationship("Teams")
    roleFK = relationship("Roles")
