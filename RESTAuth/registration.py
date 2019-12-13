from RESTAuth.serializers import RegistrationSerializer
from RESTAuth.models import RegistrationMessage
from RESTAuth.serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from RESTAuth.tokens import account_activation_token
from django.template.loader import render_to_string


def sign_up(user):
    serialized_user = UserSerializer(data=user)
    succes = False

    if serialized_user.is_valid():
        user = User.objects.create_user(username=serialized_user.data["username"], email=serialized_user.data["email"], password=serialized_user.data["password"])
        user.is_active = False
        user.save()
        send_activation_message(user)
        succes = True

    message = RegistrationMessage(succes)
    serialized_msg = RegistrationSerializer(message)
    return serialized_msg


def send_activation_message(user):
    token = account_activation_token.generate_token(user)
    domain = '127.0.0.1:8000'
    message = render_to_string("account_activation_message.html", {
        "user": user,
        "token": token,
        "domain": domain
    })
    send_mail("Profil aktiválása", message, "kriptomonitor@gmail.com", [user.email], fail_silently=False)