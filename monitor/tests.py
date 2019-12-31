from django.contrib.auth.models import User
from django.utils import timezone
from monitor.models import Transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from monitor.serializers import TransactionSerializer


class MonitorTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="User", password="1234567", email="example@gmail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))
        self.other_user = User.objects.create(username="User2", password="7654321", email="example2@gmail.com")
        Token.objects.create(user=self.other_user)

        self.quantity = 22
        self.price = 3412
        self.actual_time = timezone.now()

    def test_can_create_new_transaction(self):
        response = self.client.post("/api/create-transaction/",
                                    {"quantity": self.quantity, "purchase_price": self.price, "date_of_purchase": self.actual_time, "owner": self.user.pk},
                                    format="json")
        trans_id = response.data.get("id")
        transaction = Transaction.objects.get(pk=trans_id)
        serialized_trans = TransactionSerializer(transaction)
        self.assertEqual(serialized_trans.data, response.data)

    def test_user_cannot_create_transaction_with_other_owner(self):
        response = self.client.post("/api/create-transaction/",
                                    {"quantity": self.quantity, "purchase_price": self.price, "date_of_purchase": self.actual_time,
                                     "owner": self.other_user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_transaction_when_owner_is_doesnt_exist(self):
        response = self.client.post("/api/create-transaction/",
                                    {"quantity": self.quantity, "purchase_price": self.price, "date_of_purchase": self.actual_time,
                                     "owner": -1},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_empty_transaction(self):
        response = self.client.post("/api/create-transaction/",
                                    {"quantity": None, "purchase_price": None,
                                     "date_of_purchase": None,
                                     "owner": self.user.pk},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)