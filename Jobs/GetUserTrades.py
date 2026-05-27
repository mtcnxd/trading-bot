from database import SessionLocal
from Services.BitsoService import BitsoService
from Services.Telegram import Telegram
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

console = Console()

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        trades = bitsoService.get_user_trades()
        
        table = Table(title="User Trades", style="dim", show_header=True, header_style="bold magenta")

        table.add_column("Book", style="dim")
        table.add_column("Major")
        table.add_column("Minor")
        table.add_column("Major Currency")
        table.add_column("Minor Currency")
        table.add_column("Price")
        table.add_column("Side")
        table.add_column("Fees Amount")
        table.add_column("Tid")
        table.add_column("Oid")
        table.add_column("Created at")
        
        for trade in trades:
            table.add_row(
                trade['book'],
                trade['major'],
                trade['minor'],
                trade['major_currency'],
                trade['minor_currency'],
                trade['price'],
                trade['side'],
                trade['fees_amount'],
                trade['tid'],
                trade['oid'],
                trade['created_at'],
            )

        console.print(table)

    except Exception as e:
        console.print(f"FAILED UPDATE USER TRADES | MESSAGE: {e}")
        Telegram().send_message(f"FAILED UPDATE USER TRADES | MESSAGE: {e}")
        session.rollback()

    finally:
        session.close()

