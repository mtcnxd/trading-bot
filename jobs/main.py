from database import SessionLocal
from APIs.Bitso import Bitso
from Services.BitsoService import BitsoService
from Models import Books
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bitso = Bitso()
bitsoService = BitsoService()

with SessionLocal() as session:
    try:
        ticker = bitso.get_ticker()

        mybooks = session.query(Books).filter(Books.favorite == True).all()
        favorites = [book.book for book in mybooks]

        bitsoService.save_ticker(session, ticker, favorites)
        
    except Exception as e:
        print(f"Error: {e}")
        logger.info(e)

    finally:
        session.close()
        logger.info("session closed")