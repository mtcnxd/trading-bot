from database import SessionLocal
from APIs.Bitso import Bitso
from Services.BitsoService import BitsoService
from Models import Books
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bitso = Bitso()

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
        
    except Exception as e:
        logger.info(e)
        session.rollback()

    finally:
        session.close()
        logger.info("session closed")