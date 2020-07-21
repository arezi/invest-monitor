
import json
from datetime import datetime

import requests


import logging
logger = logging.getLogger('quote_current_crypto_foxbit')



class QuoteCurrentCrypto:

    def quote(self):

        logger.info('Quoting cryptocurrency')

        try:
            rs_dto = requests.get('https://watcher.foxbit.com.br/api/Ticker/' ).json()
        except Exception as err:
            logger.error("OS error: {0}".format(err))
            return None

        quotes = {}

        for ca in rs_dto:
            cod = None

            if ca['currency'] == 'BRLXBTC' and ca['exchange'] == 'Foxbit':
                cod = 'BTCBRL'

            if ca['currency'] == 'BTCXTUSD' and ca['exchange'] == 'Foxbit':
                cod = 'BTCUSD'

            if cod == None:
                continue

            q = {}
            q['datetime'] = ca['createdDate'].replace('T',' ').split('.')[0]
            q['price'] = float(ca['last']) 
            q['lastVariation'] = float(ca['lastVariation']) # ?? variacao hoje ?
            q['min'] = float(ca['low'])
            q['max'] = float(ca['high'])
            q['vol'] = float(ca['vol']) # ?volume de negociacao hoje?

            quotes[cod] = q

        return quotes


# quick test
#rs = quote()
#print(json.dumps(rs, indent=4))
