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

    def get_last_book_statistics(self, book_id):
        return self.session.query(BookStatistics).filter(BookStatistics.book_id == book_id).order_by(BookStatistics.id.desc()).first()

    def save_book_changes(self, last_ticker_info):
        self.logger.info(last_ticker_info.last)

        new_statistic = BookStatistics(
            book_id = last_ticker_info.book_id,
            last_value = last_ticker_info.last,
            current_value = last_ticker_info.last,
            change_value = None,
            change_percentage = None
        )

        self.session.add(new_statistic)
        self.session.commit()