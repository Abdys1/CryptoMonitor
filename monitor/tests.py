from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from monitor.models import Transaction


class MonitorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="User", email="example@gmail.com", password="123456")

    def test_can_create_new_transaction(self):
        actual_time = timezone.now()
        quantity = 22
        price = 3412
        trans = Transaction.create(quantity=quantity, purchase_price=price, date_of_purchase=actual_time, owner=self.user)
        trans.save()
        self.assertIsNotNone(trans.id)
        self.assertEqual(trans.quantity, quantity)
        self.assertEqual(trans.actual_price, price)
        self.assertEqual(trans.date_of_purchase, actual_time)
        self.assertEqual(trans.owner, self.user)