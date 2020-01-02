from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    quantity = models.IntegerField(null=False, default=0)
    purchase_price = models.IntegerField(null=False, default=0)
    date_of_purchase = models.DateTimeField(null=False, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "(quantity=" + str(self.quantity) + \
               ", purchase_price=" + str(self.purchase_price) + \
               ", date_of_purchase=" + str(self.date_of_purchase) + \
               ", owner=" + str(self.owner) + ")"