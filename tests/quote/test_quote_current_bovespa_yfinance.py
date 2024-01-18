from unittest import TestCase


from app.quote.quote_current_bovespa_yfinance import QuoteCurrentBovespaYfinance



class TestQuoteCurrentBovespaYfinance(TestCase):

    def test_quote_current_bovespa_yfinance(self):
        service = QuoteCurrentBovespaYfinance()
        quotes = service.quote(['PETR3', 'BBAS3', 'ELET3'])

        self.assertEqual(len(quotes.keys()), 3)
        self.assertIn('price', quotes['PETR3'])
        self.assertIn('variation', quotes['BBAS3'])
        self.assertIn('datetime', quotes['ELET3'])

