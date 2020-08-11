
import os
import inspect

from . import QuoteCurrentBovespaBase, QuoteCurrentCryptoBase




def __load_quote_module(mod_name, expected_subclass):
    mod = __import__(mod_name, fromlist=[mod_name])
    for attr in dir(mod):
        clss = getattr(mod, attr)
        if inspect.isclass(clss) and issubclass(clss, expected_subclass) and clss != expected_subclass:
            return clss()
    raise Exception('Not found subclass of '+str(expected_subclass)+' in '+mod_name)



quote_current_exchanges = {}

mod_current_bovespa = 'app.quote.quote_current_bovespa_bvbmf' if 'INVEST_MONITOR_MOD_QUOTE_CURRENT_BOVESPA' not in os.environ else os.environ['INVEST_MONITOR_MOD_QUOTE_CURRENT_BOVESPA']
quote_current_exchanges['BOVESPA'] = __load_quote_module(mod_current_bovespa, QuoteCurrentBovespaBase)

mod_current_bovespa = 'app.quote.quote_current_crypto_foxbit' if 'INVEST_MONITOR_MOD_QUOTE_CURRENT_CRYPTO' not in os.environ else os.environ['INVEST_MONITOR_MOD_QUOTE_CURRENT_CRYPTO']
quote_current_exchanges['CRYPTO'] = __load_quote_module(mod_current_bovespa, QuoteCurrentCryptoBase)



def get_quote_current(stock_exchanges):
    return quote_current_exchanges[stock_exchanges]
