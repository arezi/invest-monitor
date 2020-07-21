

from .quote_current_bovespa_bvbmf   import QuoteCurrentBovespaBvbmf
#from .quote_current_bovespa_easynv  import QuoteCurrentBovespaEasynv
#from .quote_current_bovespa_alphavantage  import QuoteCurrentBovespaAlphavantage

from .quote_current_crypto_foxbit import QuoteCurrentCrypto



quote_current_exchanges = {
    'BOVESPA': QuoteCurrentBovespaBvbmf(),
    'CRYPTO' : QuoteCurrentCrypto()
}


def get_quote_current(stock_exchanges):
    return quote_current_exchanges[stock_exchanges]
