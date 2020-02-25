import json
from asyncio.exceptions import CancelledError, TimeoutError

import pytest
import requests
from unittest.mock import patch

from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.core.exceptions import ObjectDoesNotExist

from CryptoMonitor import routing
from .serializers import TransactionSerializer
from .models import Transaction
from .service import market, CryptoMarket
from channels.db import database_sync_to_async


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

        self.url = "/api/transaction"

    def test_can_create_new_transaction(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "buy_amount": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": self.user.pk},
                                    format="json")
        trans_id = response.data.get("id")
        transaction = Transaction.objects.get(pk=trans_id)
        serialized_trans = TransactionSerializer(transaction)
        self.assertEqual(serialized_trans.data, response.data)

    def test_can_create_new_transaction_with_float_quantity(self):
        response = self.client.post(self.url,
                                    {"quantity": 23.22,
                                     "buy_amount": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": self.user.pk},
                                    format="json")
        trans_id = response.data.get("id")
        transaction = Transaction.objects.get(pk=trans_id)
        serialized_trans = TransactionSerializer(transaction)
        self.assertEquals(serialized_trans.data.get("quantity"), response.data.get("quantity"))
        self.assertTrue(isinstance(response.data.get("quantity"), float))

    def test_user_cannot_create_transaction_with_other_owner(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "buy_amount": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": self.other_user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_transaction_when_owner_is_doesnt_exist(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "buy_amount": self.price,
                                     "date_of_purchase": self.actual_time,
                                     "owner": -1},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_create_empty_transaction(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": None,
                                     "buy_amount": None,
                                     "date_of_purchase": None,
                                     "owner": self.user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_transaction_with_float_buy_amount(self) -> None:
        response = self.client.post(self.url,
                                    {"quantity": self.quantity,
                                     "buy_amount": 7321.23,
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
        Transaction.objects.create(quantity=213, buy_amount=3213, date_of_purchase=self.actual_time,
                                   owner=self.user)
        Transaction.objects.create(quantity=7400, buy_amount=22, date_of_purchase=self.actual_time, owner=self.user)

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
        Transaction.objects.create(quantity=213, buy_amount=3213, date_of_purchase=self.actual_time,
                                   owner=self.other_user)
        user_transactions = [
            Transaction.objects.create(quantity=22, buy_amount=7400, date_of_purchase=self.actual_time,
                                       owner=self.user),
            Transaction.objects.create(quantity=200, buy_amount=3000, date_of_purchase=self.actual_time,
                                       owner=self.user)]
        serialized_transactions = TransactionSerializer(user_transactions, many=True)
        response = self.client.get(self.url)
        self.assertListEqual(serialized_transactions.data, response.data)

    def test_when_has_11_transaction_and_get_first_page_then_return_first_ten_transaction(self):
        first_ten_trans = []
        for i in range(10):
            trans = Transaction.objects.create(quantity=213,
                                               buy_amount=3213,
                                               date_of_purchase=self.actual_time,
                                               owner=self.user)
            first_ten_trans.append(trans)
        last_trans = Transaction.objects.create(quantity=5,
                                                buy_amount=7000,
                                                date_of_purchase=self.actual_time,
                                                owner=self.user)

        response = self.client.get(self.url + "?page_num=1")
        ord_dicts = response.data["transactions"]
        result_trans = self.transactionOrderDictToList(ord_dicts)
        self.assertListEqual(result_trans, first_ten_trans)

        response = self.client.get(self.url + "?page_num=2")
        ord_dicts = response.data["transactions"]
        result_trans = self.transactionOrderDictToList(ord_dicts)
        self.assertListEqual(result_trans, [last_trans])
        self.assertEquals(response.data["pageCount"], 2)

    def transactionOrderDictToList(self, ord_dicts):
        result = []
        for ord_dict in ord_dicts:
            user = User.objects.get(pk=ord_dict["owner"])
            trans = Transaction(pk=ord_dict["id"],
                                quantity=ord_dict["quantity"],
                                buy_amount=ord_dict["buy_amount"],
                                date_of_purchase=ord_dict["date_of_purchase"],
                                owner=user)
            result.append(trans)
        return result

    def test_when_not_modify_transaction_then_return_original_transaction(self):
        trans = Transaction.objects.create(quantity=213, buy_amount=3213.0, date_of_purchase=self.actual_time,
                                           owner=self.user)
        serialized_trans = TransactionSerializer(trans)
        response = self.client.put(self.url + "/" + str(trans.pk), serialized_trans.data)
        self.assertDictEqual(response.data, serialized_trans.data)

    def test_when_modify_transaction_then_return_new_transaction(self):
        trans = Transaction.objects.create(quantity=213.22, buy_amount=3213.0, date_of_purchase=self.actual_time,
                                           owner=self.user)
        new_trans = Transaction(id=-1, quantity=2, buy_amount=9000.0, date_of_purchase=self.actual_time, owner=self.user)
        serialized_trans = TransactionSerializer(new_trans)
        response = self.client.put(self.url + "/" + str(trans.pk), serialized_trans.data)
        modified_trans = Transaction(pk=trans.pk,
                                     quantity=new_trans.quantity,
                                     buy_amount=new_trans.buy_amount,
                                     date_of_purchase=new_trans.date_of_purchase,
                                     owner=trans.owner)
        serialized_trans = TransactionSerializer(modified_trans)
        self.assertDictEqual(response.data, serialized_trans.data)

    def test_cannot_set_other_user_when_modify_transaction(self):
        trans = Transaction.objects.create(quantity=213, buy_amount=3213.0, date_of_purchase=self.actual_time,
                                           owner=self.user)
        new_trans = Transaction(id=-1, quantity=2, buy_amount=9000.0, date_of_purchase=self.actual_time, owner=self.other_user)
        serialized_trans = TransactionSerializer(new_trans)
        response = self.client.put(self.url + "/" + str(trans.pk), serialized_trans.data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_when_close_transaction_then_profit_and_date_of_sell_in_response(self):
        trans = Transaction.objects.create(quantity=self.quantity,
                                           buy_amount=self.price,
                                           date_of_purchase=self.actual_time,
                                           owner=self.user)

        new_trans = Transaction(quantity=trans.quantity,
                                buy_amount=trans.buy_amount,
                                date_of_purchase=trans.date_of_purchase,
                                owner=trans.owner,
                                date_of_sell=timezone.now(),
                                sell_price=9402)

        serializer = TransactionSerializer(new_trans)
        response = self.client.put(self.url + "/" + str(trans.pk), serializer.data)
        closed_trans = Transaction.objects.get(pk=trans.pk)
        serializer = TransactionSerializer(closed_trans)
        self.assertIsNotNone(response.data.get("date_of_sell"))
        self.assertIsNotNone(response.data.get("sell_price"))
        self.assertDictEqual(response.data, serializer.data)

    #TODO Ha nem adom meg egyszerre mindkettőt, akkor dobjon hibát

    def test_can_delete_transaction(self):
        trans = Transaction.objects.create(quantity=self.quantity,
                                           buy_amount=self.price,
                                           date_of_purchase=self.actual_time,
                                           owner=self.user)
        response = self.client.delete(self.url + "/" + str(trans.pk))
        try:
            Transaction.objects.get(pk=trans.pk)
            self.fail("Transaction is still alive!")
        except ObjectDoesNotExist:
            self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cannot_delete_when_the_trans_not_exist(self):
        trans = Transaction.objects.create(quantity=self.quantity,
                                           buy_amount=self.price,
                                           date_of_purchase=self.actual_time,
                                           owner=self.user)
        self.client.delete(self.url + "/" + str(trans.pk))
        response = self.client.delete(self.url + "/" + str(trans.pk))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_other_users_trans(self):
        trans = Transaction.objects.create(quantity=self.quantity,
                                           buy_amount=self.price,
                                           date_of_purchase=self.actual_time,
                                           owner=self.other_user)
        response = self.client.delete(self.url + "/" + str(trans.pk))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class CryptoMarketAPITest(TestCase):
    def test_has_response_when_get_exchange_rate(self) -> None:
        self.assertIsNotNone(market.get_exchange_rate())

    def test_the_return_type_is_float_when_get_exchange_rate(self) -> None:
        is_float = isinstance(market.get_exchange_rate(), float)
        self.assertTrue(is_float)

    def test_when_get_exchange_rate_then_return_right_exchange_rate(self) -> None:
        req_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        mark_response = market.get_exchange_rate()
        if abs(float(req_response.json().get("price")) - mark_response) > 5:
            self.fail("Not right exchange rate!")


@pytest.mark.asyncio
async def test_cannot_connect_to_ws_when_not_authorized():
    try:
        communicator = WebsocketCommunicator(routing.application, "/ws/exchangeRate")
        await communicator.connect()
        await communicator.disconnect()
        raise AssertionError("Successful connecting without authentication")
    except (CancelledError, TimeoutError):
        assert True


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_can_connect_and_send_message_to_ws_when_authorized():
    user = await database_sync_to_async(User.objects.create)(username="User6", password="1234567",
                                                             email="example6@gmail.com")
    token = await database_sync_to_async(Token.objects.create)(user=user)

    token_str = "Authorization=Token " + str(token) + "; csrftoken=123123124asdsar"
    headers = [(b"cookie", token_str.encode())]
    try:
        communicator = WebsocketCommunicator(routing.application, "/ws/exchangeRate", headers=headers)
        await communicator.connect()
        await communicator.send_to(text_data="Hello")
        response = await communicator.receive_from()
        await communicator.disconnect()
        assert response is not None
    except (CancelledError, TimeoutError):
        raise AssertionError("Cannot connect with token!")


@pytest.fixture
@pytest.mark.asyncio
async def get_communicator(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user, created = await database_sync_to_async(User.objects.get_or_create)(username="User5", password="1234567",
                                                                                 email="example5@gmail.com")
        token, created = await database_sync_to_async(Token.objects.get_or_create)(user=user)
        token_str = "Authorization=Token " + str(token)
        headers = [(b"cookie", token_str.encode())]
        return WebsocketCommunicator(routing.application, "/ws/exchangeRate", headers=headers)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_when_disconnect_then_cannot_send_message(get_communicator):
    communicator = get_communicator
    try:
        await communicator.connect()
        await communicator.disconnect()
        await communicator.send_to(text_data="Hello")
        response = await communicator.receive_from()
        raise AssertionError("Can send message after disconnect")
    except:
        assert True


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_when_send_get_exchange_rate_then_response_actual_exchange_rate(get_communicator):
    actual_exchange_rate = 7321.0
    with patch.object(CryptoMarket, 'get_exchange_rate', return_value=actual_exchange_rate) as mock_exchange_rate_call:
        communicator = get_communicator
        await communicator.connect()
        await communicator.send_to(text_data="get_exchange_rate")
        response = await communicator.receive_from()
        mock_exchange_rate_call.assert_called_once_with()
        await communicator.disconnect()
        assert float(response) == actual_exchange_rate


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_when_send_undefined_message_to_ws_then_send_wrong_message(get_communicator):
    communicator = get_communicator
    await communicator.connect()
    await communicator.send_to(text_data="saqwe")
    response = await communicator.receive_from()
    await communicator.disconnect()
    assert response == "wrong_msg"