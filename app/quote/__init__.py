
from abc import ABC, abstractmethod

class QuoteCurrentBovespaBase(ABC):
    stock_exchange = 'BOVESPA'
    @abstractmethod
    def quote(self, ticker_list):
        pass


class QuoteCurrentCryptoBase:
    stock_exchange = 'CRYPTO'
