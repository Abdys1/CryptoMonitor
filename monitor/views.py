from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from monitor.serializers import TransactionSerializer
from monitor.models import Transaction
from monitor.service import market
from monitor.exceptions import CannotGetMarketInfo


class TransactionDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs) -> Response:
        try:
            user = request.user
            user_token = Token.objects.get(user=user)
            owner_id = request.data.get("owner")
            owner = User.objects.get(pk=owner_id)
            owner_token = Token.objects.get(user=owner)

            if user_token == owner_token:
                return self.create(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request) -> Response:
        user = request.user
        transactions = Transaction.objects.filter(owner=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(data=serializer.data)


@api_view(['GET'])
def exchange_rate(request) -> Response:
    try:
        price = market.get_exchange_rate()
        return Response(data={"exchange_rate": price})
    except CannotGetMarketInfo:
        return Response(status=status.HTTP_424_FAILED_DEPENDENCY)