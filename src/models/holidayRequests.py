from db.database import Base
from sqlalchemy import ForeignKey, String, Integer, Column, Date, Boolean
from sqlalchemy.orm import relationship


class HolidayRequests(Base):
    """Holiday Request Model"""

    __tablename__ = "HolidayRequests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    time_of_day = Column(String(2), nullable=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    team_name = Column(String, ForeignKey("Teams.name"))
    approved = Column(Boolean, unique=False)

    teamFK = relationship("Teams")
    userFK = relationship("Users")
