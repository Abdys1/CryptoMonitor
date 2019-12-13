from django.contrib.auth.tokens import PasswordResetTokenGenerator
import hashlib


class Tokenizer:
    def generate_token(self, user):
        return str(hashlib.md5(user.username.encode()).hexdigest())


account_activation_token = Tokenizer()
