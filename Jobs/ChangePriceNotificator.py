from database import SessionLocal
from Models import Ticker

with SessionLocal() as session:
    try:
        results = {}
        results = session.query(Ticker).filter(Ticker.book_id == 2).order_by(Ticker.id.desc()).limit(2).all()
        
        for result in results:
            print(f"{result.created_at} - {result.last}")
    
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        exit()

