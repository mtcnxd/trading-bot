from database import SessionLocal
from Services.TradingService import TradingService
from Models import Ticker
from rich.console import Console
from rich.panel import Panel
from sqlalchemy import func

console = Console()

with SessionLocal() as session:
    try:
        average = session.query(func.avg(Ticker.last))\
            .filter(Ticker.book == "btc_usdt")\
            .order_by(Ticker.created_at.desc())\
            .limit(5)\
            .scalar()

        console.print(Panel(f"Average price: {average:.2f}"))

        results = session.query(Ticker)\
            .filter(Ticker.book == "btc_usdt")\
            .order_by(Ticker.id.desc())\
            .limit(3)\
            .all()
        
        for result in results:
            falling_percentage = ((result.last - result.high) / result.high) * 100
            raising_percentage = ((result.last - result.low) / result.low) * 100

            console.print(f"{result.created_at} | Low: {result.low} - Current: {result.last} - High: {result.high} | From low to last: {raising_percentage:.2f}% | From high to last: {falling_percentage:.2f}%")
    
    except Exception as e:
        console.print(f"ERROR: {e}")
        session.rollback()
        exit()

