from RESTAuth.serializers import UserSerializer
from RESTAuth.tokens import account_activation_token
from django.contrib.auth import authenticate, login

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User


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
            user.is_active = False
            user.save()
            self.send_activation_message(user)
            success = True
        else:
            success = False
            self.errors = serialized_user.errors

        return success

    def send_activation_message(self, user) -> None:
        token = account_activation_token.generate_token(user)
        domain = '127.0.0.1:8000'
        message = render_to_string("account_activation_message.html", {
            "user": user,
            "token": token,
            "domain": domain
        })
        send_mail("Profil aktiválása", message, "kriptomonitor@gmail.com", [user.email], fail_silently=False)


def activate_user(activation_token) -> bool:
    all_user = User.objects.all()
    success = False
    for user in all_user:
        actual_activation_token = account_activation_token.generate_token(user)
        if actual_activation_token == activation_token:
            success = True
            user.is_active = True
            user.save()
            break

    return success


class UserLoginHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.messages = {}

    def login_user(self, username, password) -> bool:
        self.messages = {}
        user = authenticate(request=self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            success = True
            self.messages["username"] = user.username
        else:
            self.messages["error"] = "Helytelen belépési adatok!"
            success = False

        return success