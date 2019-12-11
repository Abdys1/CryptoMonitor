from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticate.service import RegistrationHandler


class UserRegistration(APIView):
    pass
    #def get(self, request, format=None):
        #reg_handler = RegistrationHandler()
        #msg = reg_handler.registrate(user)
        #return Response(msg.data)
