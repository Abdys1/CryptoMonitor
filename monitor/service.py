import requests

from monitor.exceptions import CannotGetMarketInfo


class CryptoMarket:
    def __init__(self) -> None:
        self._url = "https://api.binance.com/api/v3"

    def get_exchange_rate(self) -> float:
        response = requests.get(self._url + "/ticker/price?symbol=BTCUSDT")
        if response.status_code == 200:
            price = float(response.json().get("price"))
            return price
        else:
            raise CannotGetMarketInfo("Cannot get exchange rate!")


market = CryptoMarket()