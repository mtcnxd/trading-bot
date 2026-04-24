from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime

class TickerInfo(Base):
    __tablename__ = "ticker_info"

    id = Column(Integer, primary_key=True)
    book = Column(String(50))
    high = Column(String(50))
    low = Column(String(50))
    last = Column(String(50))
    volume = Column(String(50))
    change_24 = Column(String(50))
    json = Column(String(1000))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())