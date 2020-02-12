from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    quantity = models.FloatField(null=False, default=0)
    purchase_price = models.FloatField(null=False, default=0)
    date_of_purchase = models.DateTimeField(null=False, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_sell = models.DateTimeField(null=True)
    sell_price = models.FloatField(null=True)

    def __str__(self) -> str:
        return "(quantity=" + str(self.quantity) + \
               ", purchase_price=" + str(self.purchase_price) + \
               ", date_of_purchase=" + str(self.date_of_purchase) + \
               ", date_of_sell=" + str(self.date_of_sell) + \
               ", owner=" + str(self.owner) + ")"