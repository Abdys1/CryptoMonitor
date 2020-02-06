from collections import OrderedDict

from rest_framework import serializers, status
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "quantity", "purchase_price", "date_of_purchase", "date_of_sell", "owner"]

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute in [None, '']:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret
