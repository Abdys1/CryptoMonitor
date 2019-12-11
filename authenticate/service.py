from authenticate.serializer import RegistrationSerializer

from authenticate.models import RegistrationMessage


class RegistrationHandler:

    def registrate(self, user):
        success = False

        if user.email != "" and user.username != "":
            success = True

        message = RegistrationMessage(success)
        serialized_msg = RegistrationSerializer(message)
        return serialized_msg
