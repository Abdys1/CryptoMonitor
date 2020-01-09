import requests
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist

from monitor.serializers import TransactionSerializer
from monitor.models import Transaction
from monitor.service import CryptoMarket


class TransactionMonitorTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="User", password="1234567", email="example@gmail.com")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
        self.other_user = User.objects.create(username="User2", password="7654321", email="example2@gmail.com")
        Token.objects.create(user=self.other_user)

        self.quantity = 22
        self.price = 3412
        self.actual_time = timezone.now()

        self.url = "/api/transaction/"

    def test_can_create_new_transaction(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity, "purchase_price": self.price,
                                     "date_of_purchase": self.actual_time, "owner": self.user.pk},
                                    format="json")
        trans_id = response.data.get("id")
        transaction = Transaction.objects.get(pk=trans_id)
        serialized_trans = TransactionSerializer(transaction)
        self.assertEqual(serialized_trans.data, response.data)

    def test_user_cannot_create_transaction_with_other_owner(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "purchase_price": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": self.other_user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_transaction_when_owner_is_doesnt_exist(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "purchase_price": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": -1},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_empty_transaction(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": None,
                                     "purchase_price": None,
                                     "date_of_purchase": None,
                                     "owner": self.user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_transaction_with_float_purchase_price(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "purchase_price": 7321.23,
                                     "date_of_purchase": self.actual_time,
                                     "owner": self.user.pk},
                                    format="json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_when_get_transactions_then_send_list(self) -> None:
        response = self.client.get(self.url)
        self.assertIsInstance(response.data, list)

    def test_send_empty_list_when_user_has_not_transaction(self) -> None:
        response = self.client.get(self.url)
        self.assertListEqual(response.data, [])

    def test_transactions_in_list_exists_when_not_empty(self) -> None:
        Transaction.objects.create(quantity=213, purchase_price=3213, date_of_purchase=self.actual_time,
                                   owner=self.user)
        Transaction.objects.create(quantity=7400, purchase_price=22, date_of_purchase=self.actual_time, owner=self.user)

        response = self.client.get(self.url)
        transactions = response.data

        if len(transactions) > 0:
            for trans in transactions:
                try:
                    Transaction.objects.get(pk=trans.get("id"))
                except ObjectDoesNotExist:
                    self.fail("The transaction does not exist!")
        else:
            self.fail("Transactions is empty!")

    def test_get_only_the_authorized_users_transactions(self) -> None:
        Transaction.objects.create(quantity=213, purchase_price=3213, date_of_purchase=self.actual_time,
                                   owner=self.other_user)
        user_transactions = [Transaction.objects.create(quantity=22, purchase_price=7400, date_of_purchase=self.actual_time, owner=self.user),
                             Transaction.objects.create(quantity=200, purchase_price=3000, date_of_purchase=self.actual_time, owner=self.user)]
        serialized_transactions = TransactionSerializer(user_transactions, many=True)
        response = self.client.get(self.url)
        self.assertListEqual(serialized_transactions.data, response.data)


class CryptoMarketAPITest(TestCase):
    def setUp(self) -> None:
        self.market = CryptoMarket()

    def test_status_is_none_when_not_send_request(self) -> None:
        self.assertIsNone(self.market.status)

    def test_status_is_not_none_when_send_request_to_api_server(self) -> None:
        self.market.get_exchange_rate()
        self.assertIsNotNone(self.market.status)

    def test_status_is_200_when_request_is_success(self) -> None:
        self.market.get_exchange_rate()
        self.assertEqual(self.market.status, 200)

    def test_has_response_when_get_exchange_rate(self) -> None:
        self.assertIsNotNone(self.market.get_exchange_rate())

    def test_the_response_type_is_float_when_get_exchange_rate(self) -> None:
        is_float = isinstance(self.market.get_exchange_rate(), float)
        self.assertTrue(is_float)

    def test_when_get_exchange_rate_then_response_right_exchange_rate(self) -> None:
        req_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        mark_response = self.market.get_exchange_rate()
        self.assertEqual(float(req_response.json().get("price")), mark_response)