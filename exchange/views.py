import requests
import time
from django.http import JsonResponse
from django.utils.timezone import now
from .models import ExchangeRate

# External API to get exchange rate (Example: Free Exchange Rate API)
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
MIN_REQUEST_INTERVAL = 10  # 10 seconds

def get_current_usd(request):
    # Check the last request time
    last_request = ExchangeRate.objects.last()
    if last_request:
        time_since_last_request = (now() - last_request.timestamp).total_seconds()
        if time_since_last_request < MIN_REQUEST_INTERVAL:
            return JsonResponse({"error": "Wait before requesting again."}, status=429)

    # Fetch exchange rate from API
    try:
        response = requests.get(API_URL)
        data = response.json()
        usd_to_rub = data["rates"]["RUB"]
    except Exception as e:
        return JsonResponse({"error": "Failed to fetch exchange rate."}, status=500)

    # Save the exchange rate to the database
    ExchangeRate.objects.create(rate=usd_to_rub)

    # Retrieve the last 10 exchange rates
    last_10_rates = ExchangeRate.objects.order_by('-timestamp')[:10]
    rate_list = [{"timestamp": str(rate.timestamp), "rate": rate.rate} for rate in last_10_rates]

    return JsonResponse({"usd_to_rub": usd_to_rub, "last_10_rates": rate_list})
