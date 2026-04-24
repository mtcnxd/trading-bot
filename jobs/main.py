from database import SessionLocal
from Services.BitsoService import BitsoService
from rich.console import Console
from rich.table import Table
from APIs import Bitso
from Models import Books
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

bitso = Bitso()

def table(data):
    table = Table()
    table.add_column("Book", style="dim", width=12)
    table.add_column("High", style="dim", width=12)
    table.add_column("Low", style="dim", width=12)
    table.add_column("Last", style="dim", width=12)
    table.add_column("Volume", style="dim", width=12)
    table.add_column("Change 24h", style="dim", width=12)

    for item in data:
        table.add_row(
            item.book, 
            str(item.last), 
            str(item.high), 
            str(item.low), 
            str(item.volume), 
            str(item.change_24)
        )

    console.print(table)

with SessionLocal() as session:
    bitsoService = BitsoService(session)

    try:
        ticker = bitso.get_ticker()

        favorite_books = session.query(Books).filter(Books.favorite == True).all()
        favorites = {book.book : book.id for book in favorite_books}

        last_ticker_info = []
        for book_id in favorites.values():
            last_ticker_info.append(bitsoService.get_last_ticker_info(book_id=book_id))

        bitsoService.save_ticker(ticker, favorites)
        
        current_ticker_info = []
        for book_id in favorites.values():
            current_ticker_info.append(bitsoService.get_last_ticker_info(book_id=book_id))

        bitsoService.save_book_changes(last_ticker_info, current_ticker_info)

        table(last_ticker_info)
        table(current_ticker_info)
        
    except Exception as e:
        logger.info(e)
        session.rollback()

    finally:
        session.close()
        logger.info("session closed")
        console.print("session closed", style="bold red")