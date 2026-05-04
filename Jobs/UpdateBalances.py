from database import SessionLocal
from Services.BitsoService import BitsoService
from Models import BookStatistics
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        balances = bitsoService.get_balance()

        for balance in balances:
            console.print(f"Currency: {balance.currency} | Available {balance.available} | Total {balance.total}")

    except Exception as e:
        print(e)
        session.rollback()

    finally:
        session.close()

