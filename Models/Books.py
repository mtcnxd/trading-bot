from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    book = Column(String(50))
    favorite = Column(Boolean, default=False)