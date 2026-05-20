from Models import TickerInfo
from Models import BookStatistics
from Models import Balance, Trades
from APIs.Bitso import Bitso
import logging
import datetime

class BitsoService:
    def __init__(self, session):
        self.bitso = Bitso()
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

    def save_book_changes(self, last_ticker_info, curren_ticker_info, table) -> BookStatistics | None:
        table.add_column("Book", style="dim")
        table.add_column("Last value")
        table.add_column("Current value", style="green")
        table.add_column("Change value")
        table.add_column("Change percentage")

        for i in range(len(curren_ticker_info)):
            book_id = curren_ticker_info[i].book_id
            last_price = last_ticker_info[i].last
            current_price = curren_ticker_info[i].last
            difference = current_price - last_price

            new_statistic = BookStatistics(
                book_id = book_id,
                last_value = last_price,
                current_value = current_price,
                change_value = round(difference, 2),
                change_percentage = round(((difference / last_price) * 100), 2)
            )

            self.session.add(new_statistic)
            self.session.commit()

            table.add_row(
                new_statistic.book.book,
                str(new_statistic.last_value),
                str(new_statistic.current_value),
                str(round(new_statistic.change_value,2)),
                str(round(new_statistic.change_percentage,2))
            )

        return table

    def get_balance(self):
        balances = self.bitso.get_balance()

        if balances is not None:
            for balance in balances['balances']:
                if float(balance['total']) > 0.0001:

                    new_balance = Balance(
                        currency = balance['currency'],
                        available = float(balance['available']),
                        total = float(balance['total'])
                    )

                    self.session.add(new_balance)
                    self.session.commit()

        return balances

    def get_trades(self, book, limit=20):
        return self.bitso.get_trades(book, limit)

    def get_user_trades(self):
        trades = self.bitso.get_user_trades()
        
        if trades is not None:
            for trade in trades:
                existing_trade = self.session.query(Trades).filter(Trades.tid == trade['tid']).first()

                if existing_trade is None:
                    new_trade = Trades(
                        book = trade['book'],
                        major = float(trade['major']),
                        minor = float(trade['minor']),
                        major_currency = trade['major_currency'],
                        minor_currency = trade['minor_currency'],
                        price = float(trade['price']),
                        side = trade['side'],
                        fees_amount = float(trade['fees_amount']),
                        tid = trade['tid'],
                        oid = trade['oid'],
                        created_at = datetime.datetime.strptime(trade['created_at'], '%Y-%m-%dT%H:%M:%S%z')
                    )

                    self.session.add(new_trade)
                    self.session.commit()

        return trades

    def get_orders(self):
        return self.bitso.get_orders()

    def get_account_status(self):
        return self.bitso.get_account_status()
