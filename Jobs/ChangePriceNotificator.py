from database import SessionLocal
from Models import TickerInfo

with SessionLocal() as session:
    try:
        results = {}
        results = session.query(TickerInfo).filter(TickerInfo.book_id == 2).order_by(TickerInfo.id.desc()).limit(2).all()
        
        for result in results:
            print(f"{result.created_at} - {result.last}")
    
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        exit()

