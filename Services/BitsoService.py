from Models import TickerInfo

class BitsoService:
    def __init__(self):
        pass

    def save_ticker(self, session, ticker, favorites):
        for book in ticker:
            if book.get("book") in favorites:
                new_ticker = TickerInfo(
                    book = book.get("book"),
                    high = book.get("high"),
                    low = book.get("low"),
                    last = book.get("last"),
                    volume = book.get("volume"),
                    change_24 = book.get("change_24")
                )

                session.add(new_ticker)
        
        session.commit()