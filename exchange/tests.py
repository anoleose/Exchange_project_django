from django.test import TestCase
from .models import ExchangeRate
from django.urls import reverse

class TestView(TestCase):
	
	def setUp(self):
		self.url = reverse("get_current_usd")


	def test_get_current_usd_GET(self):

		response = self.client.get(self.url)

		last_request = ExchangeRate.objects.last()
		self.assertEqual(response.json()['last_10_rates'][0]['rate'], last_request.rate)
		self.assertEqual(response.headers['Content-Type'], "application/json")
		self.assertEqual(response.status_code, 200)
