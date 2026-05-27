from database import SessionLocal
from Services.TradingService import TradingService
from Services.Telegram import Telegram
from Models import Ticker
from rich.console import Console
from rich.panel import Panel
from sqlalchemy import func

console = Console()

def to_percentage(number):
    return f"{number:,.2f}%"

def to_currency(number):
    return f"${float(number):,.2f}"


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
            .limit(1)\
            .all()

        for result in results:
            falling_percentage = ((result.last - result.high) / result.high) * 100
            raising_percentage = ((result.last - result.low) / result.low) * 100

            console.print(f"{result.created_at} | Low: {result.low} - Current: {result.last} - High: {result.high} | From low to last: {raising_percentage:.2f}% | From high to last: {falling_percentage:.2f}%")

            Telegram().send_message(
                f"*Updated time:* {result.created_at} \n"
                f"*Lower price:* {to_currency(result.low)} \n"
                f"*Current price:* {to_currency(result.last)} \n"
                f"*Higher price:* {to_currency(result.high)} \n"
                f"*From low to current:* {to_percentage(raising_percentage)} \n"
                f"*From high to current:* {to_percentage(falling_percentage)} \n"
                f"*Average price:* {to_currency(average)}")

    except Exception as e:
        console.print(f"ERROR: {e}")
        Telegram().send_message(f"ERROR: {e}")
        session.rollback()
        exit()

