from database import SessionLocal
from Services.BitsoService import BitsoService
from Models import BookStatistics
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
# from rich.panel import Panel
# from Services.Sensors import Sensors

console = Console()

def show_table(statistics):
    table = Table()
    table.add_column("Book", style="dim")
    table.add_column("Last value", justify="right")
    table.add_column("Current value", style="green", justify="right")
    table.add_column("Change value")
    table.add_column("Change percentage")
    table.add_column("Created at")

    for stats in statistics:
        table.add_row(
            stats.book.book,
            str(stats.last_value),
            str(stats.current_value),
            str(stats.change_value),
            str(stats.change_percentage),
            str(stats.created_at)
        )

    return table


with SessionLocal() as session:
    bitsoService = BitsoService(session)
    #temp_sensor = Sensors().get_cpu_temperature()
    #console.print(Panel(f"CPU Temperature: {temp_sensor}", style="bold red"))

    try:
        time_query = datetime.now() - timedelta(hours=1)
        statistics = session.query(BookStatistics).filter(BookStatistics.created_at >= time_query).all()
        console.print(show_table(statistics=statistics))
        
        balance = bitsoService.get_balance()
        console.print(balance)

        bitsoService.get_account_status()
        
    except Exception as e:
        print(e)
        session.rollback()

    finally:
        session.close()

