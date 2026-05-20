from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Trades(Base):
    __tablename__ = "trades_history"

    id = Column(Integer, primary_key=True)
    book = Column(String(10))
    major = Column(Float)
    minor = Column(Float)
    major_currency = Column(String(10))
    minor_currency = Column(String(10))
    price = Column(Float)
    side = Column(String(10))
    fees_amount = Column(Float)
    tid = Column(String(20))
    oid = Column(String(20))
    created_at = Column(DateTime)