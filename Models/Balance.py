from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True)
    currency = Column(String(50))
    available = Column(Float)
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.now)