from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from rest_framework import mixins, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TransactionSerializer
from .models import Transaction


class TransactionDetail(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Transaction.objects.all()

    def post(self, request, *args, **kwargs) -> Response:
        try:
            if self.is_valid_owner(request):
                return self.create(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request) -> Response:
        user = request.user
        transactions = Transaction.objects.filter(owner=user)
        if "page_num" in request.GET:
            page_number = int(request.GET["page_num"])
            paginator = Paginator(list(transactions), 10)
            page_count = paginator.num_pages
            page = paginator.page(page_number)
            serializer = TransactionSerializer(page.object_list, many=True)
            return Response(data={"pageCount": page_count, "transactions": serializer.data})
        else:
            serializer = TransactionSerializer(transactions, many=True)
            return Response(data=serializer.data)

    def put(self, request, *args, **kwargs) -> Response:
        try:
            if self.is_valid_owner(request):
                return self.update(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk) -> Response:
        try:
            trans = Transaction.objects.get(pk=pk)
            if trans.owner.pk == request.user.pk:
                trans.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def is_valid_owner(self, request) -> bool:
        user = request.user
        user_token = Token.objects.get(user=user)
        owner_id = request.data.get("owner")
        owner = User.objects.get(pk=owner_id)
        owner_token = Token.objects.get(user=owner)

        return user_token == owner_token