from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    book = Column(String(50))
    favorite = Column(Boolean, default=False)