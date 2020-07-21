
import json
import time
from datetime import datetime, timedelta


from urllib.request import urlopen, Request


INTERVAL = 1

apikey = '56ORNX93NINA1MXI'

# alphavantage allow max 5 requests per sec.  :(

import logging
logger = logging.getLogger('quote_current_bovespa_alphavantage')


class QuoteCurrentBovespaAlphavantage:

    def quote(ticker_list):
        key_series = 'Time Series ('+str(INTERVAL)+'min)'

        quotes = {}

        for cod in ticker_list:
            if cod == 'IBOV': # nao suporta IBOV, ver se tem outro codigo q se refere
                continue

            logger.debug('Quoting '+cod)

            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+cod+'.SAO&interval='+str(INTERVAL)+'min&apikey='+apikey
            r = urlopen(Request(url)).read()
            dto = json.loads(r.decode('utf-8'))

            if not key_series in dto:
                logger.warn("Couldn't get data from "+cod+': '+json.dumps(dto))
                continue

            lst_series = list(dto[key_series].keys())
            lst_series.sort()

            ao = quotes[cod] = {}

            try:
                dhk = lst_series[-1]
                #ao['datetime'] = str(datetime.strptime(dhk, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)).split('.')[0]
                ao['datetime'] = dhk
                ao['price'] = float(dto[key_series][dhk]['4. close'])
                #ao['open'] = float(dto[key_series][dhk]['1. open'])
                #ao['max'] = float(dto[key_series][dhk]['2. high'])
                #ao['min'] = float(dto[key_series][dhk]['3. low'])
                #ao['close'] = float(dto[key_series][dhk]['4. close'])
            except ValueError:
                logger.warn('Error getting data from '+cod+' ('+dhk+')')
                #print(json.dumps(dto[key_series][dhk]))
            else:
                logger.debug(cod+' [OK] : '+format(ao['price'],'.2f'))

        return quotes




### quick test ###
'''
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s - %(message)s')

dto = QuoteCurrentBovespaAlphavantage().quote(['VVAR3', 'IRBR3', 'ELET3', 'IVVB11', 'BCFF11'])

print(json.dumps(dto, indent=4))
'''

