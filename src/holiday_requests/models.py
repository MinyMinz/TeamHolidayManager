from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Boolean, Column, Date
from sqlalchemy.orm import relationship

class HolidayRequests(Base):
    __tablename__ = "HolidayRequests"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("Teams.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    morning_or_afternoon = Column(Boolean)
    
    teamFK = relationship("Teams", foreign_keys=[team_id])  # Use string "Teams"
    userFK = relationship("Users", foreign_keys=[user_id])  # Use string "Users"

    def to_json(self):
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "morning_or_afternoon": self.morning_or_afternoon
        }