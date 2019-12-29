from django.contrib.auth.models import User
from rest_framework import mixins, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from monitor.serializers import TransactionSerializer
from rest_framework.response import Response


class TransactionDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_token = Token.objects.get(user=user)
        owner_id = request.data.get("owner")
        owner = User.objects.get(pk=owner_id)
        owner_token = Token.objects.get(user=owner)

        if user_token == owner_token:
            return self.create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)