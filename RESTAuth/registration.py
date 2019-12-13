from RESTAuth.serializers import RegistrationSerializer
from RESTAuth.models import RegistrationMessage
from RESTAuth.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


def registrate(user):
    try:
        serialized_user = UserSerializer(data=user)
        serialized_user.is_valid(raise_exception=True)
        message = RegistrationMessage(True)
        user = User.objects.create_user(username=serialized_user.data["username"], email=serialized_user.data["email"], password=serialized_user.data["password"])
        user.is_active = False
        user.save()
    except ValidationError:
        message = RegistrationMessage(False)

    serialized_msg = RegistrationSerializer(message)
    return serialized_msg
