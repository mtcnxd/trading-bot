from database import SessionLocal
from Services.BitsoService import BitsoService
from rich.console import Console
from rich.table import Table
# from Services.Sensors import Sensors

console = Console()

with SessionLocal() as session:
    #temp_sensor = Sensors().get_cpu_temperature()

    try:
        bitso_service = BitsoService(session)
        account_status = bitso_service.get_account_status()
        console.print(account_status)
        
    except Exception as e:
        print(e)
        session.rollback()

    finally:
        session.close()