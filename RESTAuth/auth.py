from .serializers import UserSerializer

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserRegistrationHandler:
    def __init__(self, user_data) -> None:
        self._user_data = user_data
        self.errors = {}

    def sign_up(self) -> bool:
        serialized_user = UserSerializer(data=self._user_data)

        if serialized_user.is_valid():
            user = User.objects.create_user(username=serialized_user.data["username"],
                                            email=serialized_user.data["email"],
                                            password=serialized_user.data["password"])
            user.is_active = True
            user.save()
            Token.objects.create(user=user)
            success = True
        else:
            success = False
            self.errors = serialized_user.errors

        return success
