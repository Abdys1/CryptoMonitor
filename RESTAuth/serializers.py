from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        try:
            user_with_same_email = User.objects.get(email=value)
        except:
            user_with_same_email = None

        if value == "":
            raise ValidationError("Adjon meg egy email címet!")
        if user_with_same_email is not None:
            raise ValidationError("Létezik már egy felhasználó ezzel az e-mail címmel!")
        return value

    def validate_username(self, value):
        if len(value) < 4:
            raise ValidationError("Túl rövid felhasználónév!")
        return value

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active"]
