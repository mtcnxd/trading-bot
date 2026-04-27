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
    updated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())

    book = relationship("Books", back_populates="book_stats")
