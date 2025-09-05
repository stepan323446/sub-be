from requests import Response
from django.urls import reverse_lazy
from unittest.mock import patch
from project.utils import StrAPITestCase

# Create your tests here.
class CurrencyTest(StrAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        # Fake GET to exchange api
        self.requests_get_patcher = patch("currency.utils.requests.get")
        self.mock_get = self.requests_get_patcher.start()
        with open('currency/mocks/currency_list.json') as f: mock_data = f.read()

        response = Response()
        response.status_code = 200
        response._content = mock_data.encode("utf-8")

        self.mock_get.return_value = response

    def tearDown(self):
        self.requests_get_patcher.stop()
        super().tearDown()

    def test_refresh_currency_restrict(self):
        self.authorize()
        url = reverse_lazy('currency-refresh')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.mock_get.assert_not_called()

    def test_refresh_currency(self):
        self.admin_authorize()
        url = reverse_lazy('currency-refresh')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.mock_get.assert_called_once()

    def test_cached_currency_list(self):
        self.authorize()
        url = reverse_lazy('currency-list')
        
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_get.call_count, 1)