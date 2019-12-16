from RESTAuth.models import RegistrationMessage, LoginMessage

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationMessage
        fields = ["success"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginMessage
        fields = ["success", "username"]


class UserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["email"] == "" or len(attrs["username"]) < 4:
            raise ValidationError("Not valid user")
        return attrs

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active"]
