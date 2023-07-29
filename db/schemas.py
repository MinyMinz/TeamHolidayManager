from sqlalchemy import ForeignKey, String, Integer, Column
from sqlalchemy.orm import relationship

from .database import Base

class Roles(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"Roles(id={self.id!r}, name={self.name!r}, description={self.description!r}))"

class Team(Base):
    __tablename__ = "Teams"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    #useful for debugging
    def __repr__(self):
        return f"Team(id={self.id!r}, name={self.name!r}, description={self.description!r}))"

class User(Base): 
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    fullName = Column(String)
    email =  Column(String)
    password = Column(String)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    role_id =  Column(Integer, ForeignKey("Roles.id"))

    team = relationship("Team")
    role = relationship("Role")
    
    #useful for debugging
    def __repr__(self):
        return f"User(id={self.id!r}, fullName={self.fullName!r}, email={self.email!r}, password={self.password!r}, Roles={self.Roles!r}))"
    
class AnnualLeave(Base):
    __tablename__ = "AnnualLeave"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    name = Column(String)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)

    team = relationship("Team")
    user = relationship("User")

    #useful for debugging
    def __repr__(self):
        return f"teamCalendar(id={self.id!r}, team_id={self.team_id!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, start_date={self.start_date!r}, end_date={self.end_date!r}))"    
