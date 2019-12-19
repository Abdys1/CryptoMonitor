from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from RESTAuth.auth import UserRegistrationHandler, UserLoginHandler


class ActivateRegistration(APIView):
    pass


class UserLogin(APIView):
    def post(self, request) -> Response:
        username, email, password = request.data.values()
        login_handler = UserLoginHandler(request)
        login_handler.login_user(username=username, password=password)
        return Response(data=login_handler.messages, status=status.HTTP_200_OK)


class UserRegistration(APIView):
    def post(self, request, format=None) -> Response:
        reg = UserRegistrationHandler(request.data)
        success = reg.sign_up()
        if success:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=json.dumps(reg.errors), status=status.HTTP_200_OK)