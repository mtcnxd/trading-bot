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
        trading_service = TradingService()

        prices = session.query(Ticker.last)\
            .filter(Ticker.book == "btc_usdt")\
            .order_by(Ticker.created_at.desc())\
            .limit(24)\
            .all()

        prices = [price[0] for price in prices]

        sma = trading_service.sma(prices)
        ema = trading_service.ema(prices, periods=10)

        console.print(Panel(f"Simple Moving Average: {sma:.2f}"))

        result = session.query(Ticker)\
            .filter(Ticker.book == "btc_usdt")\
            .order_by(Ticker.id.desc())\
            .limit(1)\
            .first()

        raising_percentage = ((result.last - result.low) / result.low) * 100
        falling_percentage = ((result.last - result.high) / result.high) * 100

        console.print(f"SMA 24h: {to_currency(sma)}")
        console.print(f"EMA 10h: {to_currency(ema)}")
        console.print(f"LAST: {to_currency(result.last)}")

        Telegram().send_message(
            f"*Updated at:* {result.created_at} \n"
            f"*Lower:* {to_currency(result.low)} \n"
            f"*Current:* {to_currency(result.last)} \n"
            f"*Average 24hs:* {to_currency(sma)} \n"
            f"*Higher:* {to_currency(result.high)} \n"
            f"*From low to current:* {to_percentage(raising_percentage)} \n"
            f"*From high to current:* {to_percentage(falling_percentage)} \n")

        if result.low == result.last:
            Telegram().send_message("The price has reached the lower limit")

    except Exception as e:
        console.print(f"ERROR: {e}")
        Telegram().send_message(f"ERROR: {e}")
        session.rollback()
        exit()

