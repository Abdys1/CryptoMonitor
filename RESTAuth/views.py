from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from RESTAuth.auth import UserRegistrationHandler


class ActivateRegistration(APIView):
    pass


class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        reg = UserRegistrationHandler(request.data)
        success = reg.sign_up()
        if success:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=json.dumps(reg.errors), status=status.HTTP_200_OK)