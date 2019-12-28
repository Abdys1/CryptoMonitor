from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    quantity = models.IntegerField(null=False, default=0)
    purchase_price = models.IntegerField(null=False, default=0)
    date_of_purchase = models.DateTimeField(null=False, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create(cls, quantity, purchase_price, date_of_purchase, owner):
        trans = Transaction()
        trans.quantity = quantity
        trans.date_of_purchase = date_of_purchase
        trans.actual_price = purchase_price
        trans.owner = owner
        return trans