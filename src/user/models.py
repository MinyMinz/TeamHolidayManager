from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Boolean, Column, Date
from sqlalchemy.orm import relationship

class Roles(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    #useful for debugging
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Teams(Base):
    __tablename__ = "Teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    #useful for debugging
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class User(Base): 
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    email =  Column(String)
    password = Column(String)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    role_id =  Column(Integer, ForeignKey("Roles.id"))

    teamFK = relationship("Teams", foreign_keys=[team_id])  # Use string "Teams"
    roleFK = relationship("Roles", foreign_keys=[role_id])  # Use string "Roles"
    
    def to_json(self):
        return {
            "id": self.id,
            "fullName": self.fullName,
            "email": self.email,
            "password": self.password,
            "team_id": self.team_id,
            "role_id": self.role_id
        }