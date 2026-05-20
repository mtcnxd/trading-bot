from database import SessionLocal
from Services.BitsoService import BitsoService
from rich.console import Console
from rich.table import Table

console = Console()

with SessionLocal() as session:
    try:
        favorites = ["btc_mxn","eth_mxn","ltc_mxn","btc_usdt"]

        bitso_service = BitsoService(session)
        tickers = bitso_service.get_ticker(favorites)

        table = Table(title="Bitso Tickers", style="dim", show_header=True, header_style="bold magenta")
        
        table.add_column("Book", style="dim")
        table.add_column("High")
        table.add_column("Low")
        table.add_column("Last")
        table.add_column("Volume")
        table.add_column("Change 24h")

        for ticker in tickers:
            table.add_row(
                ticker['book'],
                ticker['high'],
                ticker['low'],
                ticker['last'],
                ticker['volume'],
                ticker['change_24']
            )

        console.print(table)

    except Exception as e:
        console.print(f"FAILED UPDATE TICKER | MESSAGE: {e}")
        session.rollback()

    finally:
        session.close()
        console.print("session closed", style="bold red")