from Models import TickerInfo
from Models import BookStatistics
import logging

class BitsoService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    def save_ticker(self, ticker, favorites):
        for ticker_book in ticker:            
            if ticker_book.get('book') in favorites.keys():
                book = ticker_book.get('book')

                new_ticker = TickerInfo(
                    book = ticker_book.get("book"),
                    book_id = favorites.get(book),
                    high = ticker_book.get("high"),
                    low = ticker_book.get("low"),
                    last = ticker_book.get("last"),
                    volume = ticker_book.get("volume"),
                    change_24 = ticker_book.get("change_24")
                )

                self.session.add(new_ticker)
        
        self.session.commit()

    def get_last_ticker_info(self, book_id):
        return self.session.query(TickerInfo).filter(TickerInfo.book_id == book_id).order_by(TickerInfo.id.desc()).first()

    def save_book_changes(self, last_ticker_info, curren_ticker_info) -> BookStatistics | None:
        for i in range(len(curren_ticker_info)):
            book_id = curren_ticker_info[i].book_id
            last_price = last_ticker_info[i].last
            current_price = curren_ticker_info[i].last
            difference = current_price - last_price

            new_statistic = BookStatistics(
                book_id = book_id,
                last_value = last_price,
                current_value = current_price,
                change_value = difference,
                change_percentage = difference / last_price * 100
            )

            self.session.add(new_statistic)
            self.session.commit()
            
            self.logger.info(f"El precio anterior de {new_statistic.book.book} fue {new_statistic.last_value} el precio actual es {new_statistic.current_value} la diferencia es {new_statistic.change_value}")
