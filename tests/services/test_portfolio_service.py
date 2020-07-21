from unittest import TestCase
from unittest.mock import patch, Mock


from app.services import portfolio_service

import json



class TestPortfolioService(TestCase):

    @patch('app.data.repositories.OperationRepository.list_active', return_value=[])
    def test_get_stocks_simple(self, mock_list_active):
        # simple empty test
        stocks = portfolio_service.get_stocks()
        self.assertEqual(len(stocks.keys()), 0)

    @patch('app.data.repositories.OperationRepository.list_active')
    def test_get_stocks_complex(self, mock_list_active):
        # complex test
        elet3_amount = 300
        mock_list_active.return_value = [
            { 'id': 1, 'ticker': 'ELET3', 'date': '2020-04-20', 'price': 20.00, 'buy': 200, 'sell': 0, 'ticker_amount': elet3_amount, 'ticker_last_operation': '2020-04-25' },
            { 'id': 2, 'ticker': 'ELET3', 'date': '2020-04-22', 'price': 23.50, 'buy': 200, 'sell': 0, 'ticker_amount': elet3_amount, 'ticker_last_operation': '2020-04-25' },
            { 'id': 3, 'ticker': 'PETR3', 'date': '2020-04-22', 'price': 10.00, 'buy': 100, 'sell': 0, 'ticker_amount': 100, 'ticker_last_operation': '2020-04-22' },
            # sold 200 ELET3
            { 'id': 5, 'ticker': 'ELET3', 'date': '2020-04-25', 'price': 22.50, 'buy': 100, 'sell': 0, 'ticker_amount': elet3_amount, 'ticker_last_operation': '2020-04-25' }
        ]
        stocks = portfolio_service.get_stocks()
        #print(json.dumps(stocks, indent=4))

        self.assertEqual(len(stocks.keys()), 2) # ELET3 and PETR3
        self.assertEqual(stocks['ELET3']['amount'], elet3_amount)
        self.assertEqual(len(stocks['ELET3']['items']), 2)

