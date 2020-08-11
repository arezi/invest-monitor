
import json
from datetime import datetime

import xml.etree.ElementTree as ET


import requests
import datetime


import logging
logger = logging.getLogger('quote_current_bovespa_bvbmf')

from . import QuoteCurrentBovespaBase



class QuoteCurrentBovespaBvbmf(QuoteCurrentBovespaBase):

    def quote(self, ticker_list):

        logger.info('Quoting '+(','.join(ticker_list)))

        url = "http://bvmf.bmfbovespa.com.br/cotacoes2000/FormConsultaCotacoes.asp?strListaCodigos="+('|'.join(ticker_list))
        header = { 'Accept': 'application/xml' }

        try:
            req = requests.get(url, headers=header)
        except Exception as err:
            logger.error("OS error: {0}".format(err))
            return None

        tree =  ET.ElementTree(ET.fromstring(req.content))
        root = tree.getroot()

        quotes = {}

        for stock_el in root:
            q = quotes[stock_el.attrib['Codigo']] = {}
            
            dh = stock_el.attrib['Data']
            q['datetime'] = str(datetime.datetime.strptime(dh, '%d/%m/%Y %H:%M:%S'))

            q['price'] = self.__str_ptbr_to_float(stock_el.attrib['Ultimo'])
            q['variation'] = self.__str_ptbr_to_float(stock_el.attrib['Oscilacao']) # variacao hoje
            q['min'] = self.__str_ptbr_to_float(stock_el.attrib['Minimo'])
            q['max'] = self.__str_ptbr_to_float(stock_el.attrib['Maximo'])
            #q['vol'] = ??

        return quotes


    def __str_ptbr_to_float(self, s):
        return float(s.replace('.','').replace(',','.'))




