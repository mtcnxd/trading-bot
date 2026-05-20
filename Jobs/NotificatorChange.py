from database import SessionLocal
from Services.TradingService import TradingService
from Models import Ticker

with SessionLocal() as session:
    try:
        results = {}
        results = session.query(Ticker)\
            .filter(Ticker.book == "btc_usdt")\
            .order_by(Ticker.id.desc())\
            .limit(2)\
            .all()
        
        for result in results:
            raising_percentage = ((result.last - result.high) / result.high) * 100
            falling_percentage = ((result.last - result.low) / result.low) * 100

            print(f"{result.created_at} | Low: {result.low} - High: {result.high} - Current: {result.last} - Falling: {falling_percentage:.2f}% - Raising: {raising_percentage:.2f}%")
    
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        exit()

