from database import SessionLocal
from Services.BitsoService import BitsoService
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        orders = bitsoService.get_orders()
        
        for order in orders:
            console.print(order)

    except Exception as e:
        console.print(f"ERROR MESSAGE: {e}", style="bold red")
        session.rollback()

    finally:
        session.close()

