from database import SessionLocal
from Services.BitsoService import BitsoService
from Models import BookStatistics
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        #trades = bitsoService.get_trades("btc_usdt", limit=10)
        trades = bitsoService.get_user_trades()
        
        for trade in trades:
            console.print(trade)

    except Exception as e:
        console.print(f"ERROR MESSAGE: {e}", style="bold red")
        session.rollback()

    finally:
        session.close()

