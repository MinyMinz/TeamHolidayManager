from db.database import Base
from sqlalchemy import  String, Integer, Column

class Roles(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100), nullable=True)