from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class TickerInfo(Base):
    __tablename__ = "ticker_info"

    id = Column(Integer, primary_key=True)
    book = Column(String(50))
    book_id = Column(Integer, ForeignKey("books.id"))
    high = Column(String(50))
    low = Column(String(50))
    last = Column(String(50))
    volume = Column(String(50))
    change_24 = Column(String(50))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())