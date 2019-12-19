from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if value == "":
            raise ValidationError("Adjon meg egy email címet!")
        return value

    def validate_username(self, value):
        if len(value) < 4:
            raise ValidationError("Túl rövid felhasználónév!")
        return value

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active"]
