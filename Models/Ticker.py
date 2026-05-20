from sqlalchemy import Column, Integer, String, Double, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Ticker(Base):
    __tablename__ = "ticker"

    id = Column(Integer, primary_key=True)
    book = Column(String(50))
    book_id = Column(Integer, ForeignKey("books.id"))
    high = Column(Double)
    low = Column(Double)
    last = Column(Double)
    volume = Column(Double)
    change_24 = Column(Double)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())