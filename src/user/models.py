from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship

class Users(Base): 
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email =  Column(String, unique=True)
    password = Column(String)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    role_id =  Column(Integer, ForeignKey("Roles.id"))

    teamFK = relationship("Teams")
    roleFK = relationship("Roles")  