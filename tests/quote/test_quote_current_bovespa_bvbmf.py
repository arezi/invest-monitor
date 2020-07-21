from unittest import TestCase


from app.quote.quote_current_bovespa_bvbmf import QuoteCurrentBovespaBvbmf

import json



class TestQuoteCurrentBovespaBvbmf(TestCase):

    def test_quote_current_bovespa_bvbmf(self):
        service = QuoteCurrentBovespaBvbmf()
        quotes = service.quote(['PETR3', 'VVAR3', 'ELET3'])

        self.assertEqual(len(quotes.keys()), 3)
        self.assertIn('price', quotes['PETR3'])
        self.assertIn('variation', quotes['VVAR3'])
        self.assertIn('datetime', quotes['ELET3'])

