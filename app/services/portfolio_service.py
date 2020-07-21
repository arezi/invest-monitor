

from datetime import datetime


#import app.quote.quote_current_bovespa_easynv as quote_current_bovespa
#import app.quote.quote_current_bovespa_bvbmf as quote_current_bovespa
from app.quote.factory import get_quote_current

from app.data import operation_repository

def get_stocks():
    
    active = operation_repository.list_active()

    # build the portfolio (stocks that haven't been sold)    
    stocks = {}
    for op in active:
        if op['ticker'] not in stocks:
            initial_diff = op['ticker_amount']-op['buy']
            stocks[ op['ticker'] ] = {
                'ticker' : op['ticker'],
                'amount' : op['ticker_amount'], 
                'last_operation' : op['ticker_last_operation'],
                'last_buy' : op['date'],
                'items' : [op],
                'diff' : initial_diff
            }
            op['amount'] = op['buy'] if op['ticker_amount'] >= op['buy'] else initial_diff
        else:
            stock = stocks[ op['ticker'] ]
            if stock['diff'] > 0:
                op['amount'] = op['buy'] if stock['diff'] >= op['buy'] else stock['diff']
                stock['items'].append(op)
                stock['diff'] = stock['diff']-op['amount']


    # remove redundant fields to clear the output
    for ticker in stocks.keys():
        del stocks[ticker]['diff']
        for op in stocks[ticker]['items']:
            del op['ticker_amount']
            del op['ticker_last_operation']

    return stocks


def quote():

    stocks = get_stocks()

    total = {'invested' : 0, 'gain' : 0, 'total' : 0, 'quote_variation_avg' : 0}

    quotator = get_quote_current('BOVESPA')
    quotes = quotator.quote(stocks.keys())

    if quotes is None:
        return {'stocks' : stocks}

    for ticker in quotes.keys():
        stocks[ticker]['quote'] = quotes[ticker]
        quote_price = quotes[ticker]['price']
        sumtk = {'price': 0, 'roi' : 0, 'invested' : 0, 'gain' : 0, 'total' : 0, 'days' : 0, 'roi_per_day' : 0}
        for op in stocks[ticker]['items']:
            op['calc'] = {}

            op['calc']['amount_ratio'] = op['amount'] / stocks[ticker]['amount']
            sumtk['price'] += op['price'] * op['calc']['amount_ratio']

            op['calc']['roi'] = (quote_price - op['price']) / op['price'] * 100  
            sumtk['roi'] += op['calc']['roi'] * op['calc']['amount_ratio']

            op['calc']['invested'] = op['amount'] * op['price']
            sumtk['invested'] += op['calc']['invested']

            op['calc']['gain'] = (quote_price - op['price']) * op['amount'] 
            sumtk['gain'] += op['calc']['gain']

            op['calc']['total'] = (op['price'] * op['amount']) + op['calc']['gain']  
            sumtk['total'] += op['calc']['total']

            op['calc']['days'] = (datetime.now() - datetime.strptime(op['date'], '%Y-%m-%d') ).days
            sumtk['days'] += op['calc']['days'] * op['calc']['amount_ratio']

            op['calc']['roi_per_day'] = (op['calc']['roi'] / op['calc']['days']) if op['calc']['days'] > 0 else op['calc']['roi']
            sumtk['roi_per_day'] += op['calc']['roi_per_day'] * op['calc']['amount_ratio']

        stocks[ticker]['calc'] = sumtk
        
        total['invested'] += sumtk['invested']
        total['gain'] += sumtk['gain']
        total['total'] += sumtk['total']
        total['quote_variation_avg'] += quotes[ticker]['variation'] if 'variation' in quotes[ticker] else 0

    total['roi'] = (total['total'] - total['invested']) / total['invested'] * 100 if total['invested'] > 0 else 0
    total['quote_variation_avg'] = total['quote_variation_avg'] / len(quotes.keys()) if len(quotes.keys()) > 0 else 0


    portfolio = {}

    portfolio['stocks'] = stocks

    portfolio['total'] = total

    return portfolio




