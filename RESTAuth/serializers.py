from django.contrib.auth.models import User
from rest_framework import serializers

from RESTAuth.models import RegistrationMessage
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationMessage
        fields = ["success"]


class UserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["email"] == "" or len(attrs["username"]) < 4:
            raise ValidationError("Not valid user")
        return attrs

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active"]
