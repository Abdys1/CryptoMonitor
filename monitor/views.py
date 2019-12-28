from rest_framework import mixins, generics, serializers, permissions

from monitor.serializers import TransactionSerializer


class TransactionDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)