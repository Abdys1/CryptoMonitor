from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from .auth import UserRegistrationHandler


class ActivateRegistration(APIView):
    pass


class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request) -> Response:
        reg = UserRegistrationHandler(request.data)
        success = reg.sign_up()
        if success:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=json.dumps(reg.errors), status=status.HTTP_200_OK)


class AccountInformation(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request) -> Response:
        user = request.user
        message = {"id": user.pk, "username": user.username, "email": user.email}
        return Response(message, status=status.HTTP_200_OK)