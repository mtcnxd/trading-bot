from Services.BitsoService import BitsoService

class TradingService:
    def __init__(self):
        pass

    def place_order(self, data:dict):
        
        order_data = {
            "book": data['book'],
            "side": "buy",
            "order_type": "limit",
            "minor": data['minor'],
            "price": data['price']
        }

    def ema(self, prices: list, periods: int = 10):
        # Formula: EMA = (Precio actual - EMA anterior) * multiplicador + EMA anterior

        if len(prices) < periods:
            raise ValueError("The list of prices is shorter than the number of periods.")

        chronological_prices = list(reversed(prices))
        
        multiplicator = 2 / (periods + 1)
        initial_sma = sum(chronological_prices[:periods]) / periods

        current_ema = initial_sma

        for price in chronological_prices[periods:]:
            current_ema = (price - current_ema) * multiplicator + current_ema

        return current_ema

    def sma(self, prices: list):
        # Formula: SMA = SUMA(Precios de cierre / Periods)
        return sum(prices) / len(prices)
    
        
