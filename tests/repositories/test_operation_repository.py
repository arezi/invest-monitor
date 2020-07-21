
from unittest.mock import patch, Mock


from app.data.repositories import OperationRepository

from . import AbstractTestRepository


class TestOperationRepository(AbstractTestRepository):

    def setUp(self):
        self.rep = OperationRepository()

    def test_list_active(self):
        self.rep.list_active()

    def test_sum_sold_current_month(self):
        self.rep.sum_sold_current_month('BOVESPA')


