import requests


class CryptoMarket:
    def __init__(self) -> None:
        self.status = None
        self._url = "https://api.binance.com/api/v3"

    def get_exchange_rate(self) -> float:
        response = requests.get(self._url + "/ticker/price?symbol=BTCUSDT")
        self.status = response.status_code
        price = float(response.json().get("price"))
        return price