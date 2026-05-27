from Models import Ticker, Balance, Trades
from APIs.Bitso import Bitso
import logging
import datetime

class BitsoService:
    def __init__(self, session):
        self.bitso = Bitso()
        self.session = session
        self.logger = logging.getLogger(__name__)

    def get_ticker(self, favorites: list) -> dict:
        tickers = self.bitso.get_ticker()

        if tickers is not None:
            for ticker in tickers:
                if ticker.get("book") not in favorites:
                    continue

                new_ticker = Ticker(
                    book = ticker.get("book"),
                    high = ticker.get("high"),
                    low = ticker.get("low"),
                    last = ticker.get("last"),
                    volume = ticker.get("volume"),
                    change_24 = ticker.get("change_24")
                )

                self.session.add(new_ticker)
                self.session.commit()

        return tickers

    def get_balance(self) -> dict :
        balances = self.bitso.get_balance()

        if balances is not None:
            for balance in balances['balances']:
                existing_balance = self.session.query(Balance).filter(Balance.currency == balance['currency']).first()

                if existing_balance is None:
                    new_balance = Balance(
                        currency = balance['currency'],
                        available = float(balance['available']),
                        total = float(balance['total'])
                    )

                    self.session.add(new_balance)
                    self.session.commit()

                else:
                    existing_balance.available = float(balance['available'])
                    existing_balance.total = float(balance['total'])
                    existing_balance.updated_at = datetime.datetime.now()
                    self.session.commit()

        return balances

    def get_user_trades(self) -> dict:
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

    def get_trades(self, book, limit=20):
        return self.bitso.get_trades(book, limit)

    def get_orders(self):
        return self.bitso.get_orders()

    def place_order(self, trade_data : dict) -> dict:
        return {}

    def get_account_status(self) -> dict:
        return self.bitso.get_account_status()
