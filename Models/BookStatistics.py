from sqlalchemy import Column, Integer, String, DateTime, Boolean, Double, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class BookStatistics(Base):
    __tablename__ = "books_statistics"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    last_value = Column(Double)
    current_value = Column(Double)
    change_value = Column(Double)
    change_percentage = Column(Double)

    #book = relationship("Book", back_populates="books_statistics")
