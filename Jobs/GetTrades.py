from database import SessionLocal
from Services.BitsoService import BitsoService
from Models import BookStatistics
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

console = Console()

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        trades = bitsoService.get_trades("btc_usdt", limit=10)
        
        table = Table(title="Trades", style="dim", show_header=True, header_style="bold magenta")

        table.add_column("Book", style="dim")
        table.add_column("Amount")
        table.add_column("Maker Side")
        table.add_column("Price")
        table.add_column("TID")
        table.add_column("Created at")

        for trade in trades:
            print(trade)

            table.add_row(
                trade['book'],
                str(trade['amount']),
                trade['maker_side'],
                str(trade['price']),
                str(trade['tid']),
                trade['created_at']
            )

        console.print(table)

    except Exception as e:
        console.print(f"ERROR MESSAGE: {e}", style="bold red")
        session.rollback()

    finally:
        session.close()

