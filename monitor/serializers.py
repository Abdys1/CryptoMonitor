from rest_framework import serializers

from monitor.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "quantity", "purchase_price", "date_of_purchase", "owner"]