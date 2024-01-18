
import yfinance as yf
import datetime


import logging
logger = logging.getLogger('quote_current_bovespa_yfinance')

from . import QuoteCurrentBovespaBase



class QuoteCurrentBovespaYfinance(QuoteCurrentBovespaBase):

    def quote(self, ticker_list):

        logger.info('Quoting '+(','.join(ticker_list)))

        yf_map = {}
        for tk in ticker_list:
            yf_map[tk] = '^BVSP' if tk == 'IBOV' else tk+'.SA'

        yf_tickets = ' '.join(yf_map.values())

        dfs = yf.download(yf_tickets, period='1d', auto_adjust = True, progress=False)

        quotes = {}

        for tk in ticker_list:
            yf_tk = yf_map[tk]
            if yf_tk not in dfs['Close'] or len(dfs['Close'][yf_tk]) == 0: # check if trading session is closed
                continue

            q = quotes[tk] = {}

            q['datetime'] = str(datetime.datetime.now()).split('.')[0]

            q['price'] = float(dfs['Close'][yf_tk].iloc[0])
            q['open'] = float(dfs['Open'][yf_tk].iloc[0])

            # TODO it would be best to consider the previous day Close rather than current Open
            q['variation'] = float( (q['price'] - dfs['Open'][yf_tk].iloc[0]) * 100 / q['price'] )

            q['min'] = float( dfs['Low'][yf_tk].iloc[0] )
            q['max'] = float( dfs['High'][yf_tk].iloc[0] )
            q['vol'] = float( dfs['Volume'][yf_tk].iloc[0] ) # optional

        return quotes





