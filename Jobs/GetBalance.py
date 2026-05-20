from database import SessionLocal
from Services.BitsoService import BitsoService
from rich.console import Console
from rich.table import Table

console = Console()

with SessionLocal() as session:
    try:
        bitso_service = BitsoService(session)
        balances = bitso_service.get_balance()

        table = Table(title="Bitso Balances", style="dim", show_header=True, header_style="bold magenta")

        table.add_column("Currency", style="dim")
        table.add_column("Available")
        table.add_column("Total")

        for balance in balances['balances']:
            if float(balance['available']) > 0.0001:
                table.add_row(
                    balance['currency'],
                    balance['available'],
                    balance['total']
                )

        console.print(table)

    except Exception as e:
        console.print(f"FAILED TO GET BALANCE | MESSAGE: {e}")
        session.rollback()

    finally:
        session.close()
        console.print("session closed", style="bold red")

