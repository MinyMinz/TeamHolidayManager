from db.database import Base
from sqlalchemy import String, Integer, Column


class Roles(Base):
    __tablename__ = "Roles"

    name = Column(String(50), primary_key=True, unique=True)
    description = Column(String(100), nullable=True)
