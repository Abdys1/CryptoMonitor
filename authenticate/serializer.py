from rest_framework import serializers

from authenticate.models import RegistrationMessage


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationMessage
        fields = ["success"]