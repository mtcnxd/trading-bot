from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
from datetime import datetime

class Balance(Base):
    __tablename__ = "balance"

    id = Column(Integer, primary_key=True)
    currency = Column(String(50))
    available = Column(Float)
    total = Column(Float)
    updated_at = Column(DateTime, default=datetime.now)