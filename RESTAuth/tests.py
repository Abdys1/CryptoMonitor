import hashlib

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from RESTAuth.serializers import RegistrationSerializer
from RESTAuth.registration import sign_up
from RESTAuth.tokens import account_activation_token


class RegistrationTest(TestCase):
    def setUp(self):
        self.valid_user = {"username": "User", "email": "example@gmail.com", "password": "1221313"}
        self.invalid_user = {"username": "User2", "email": "", "password": "1221313"}

    def test_has_reg_message(self):
        reg_message = sign_up(self.valid_user)
        self.assertIsNotNone(reg_message)

    def test_message_is_serialized(self):
        reg_message = sign_up(self.valid_user)
        is_reg_serializer = isinstance(reg_message, RegistrationSerializer)
        self.assertTrue(is_reg_serializer)

    def test_send_success_message_when_registration_is_valid(self):
        reg_message = sign_up(self.valid_user)
        self.assertTrue(reg_message.data["success"])

    def test_send_not_success_message_when_user_has_not_mail(self):
        reg_message = sign_up(self.invalid_user)
        self.assertFalse(reg_message.data["success"])

    def test_send_not_success_message_when_user_has_not_username(self):
        self.invalid_user["username"] = ""
        self.invalid_user["email"] = "example2@gmail.com"
        reg_message = sign_up(self.invalid_user)
        self.assertFalse(reg_message.data["success"])

    def test_send_not_success_message_when_email_is_not_valid(self):
        self.invalid_user["email"] = "dasda.com"
        self.invalid_user["username"] = "User1"
        reg_message = sign_up(self.invalid_user)
        self.assertFalse(reg_message.data["success"])

    def test_save_valid_user_to_the_database(self):
        sign_up(self.valid_user)
        username, email, password = self.valid_user.values()
        user = User.objects.get(username=username)
        self.assertEqual(username, user.username)
        self.assertEqual(email, user.email)

    def test_send_not_success_message_when_username_is_shorter_as_four_char(self):
        self.invalid_user["email"] = "example3@gmail.com"
        self.invalid_user["username"] = "sxd"
        reg_message = sign_up(self.invalid_user)
        self.assertFalse(reg_message.data["success"])

    def test_user_is_not_active_after_registration(self):
        username, email, password = self.valid_user.values()
        sign_up(self.valid_user)
        user = User.objects.get(username=username)
        self.assertFalse(user.is_active)

    def test_send_email(self):
        sign_up(self.valid_user)
        self.assertEqual(len(mail.outbox), 1)

    def test_send_to_user_activate_email(self):
        sign_up(self.valid_user)
        user = User.objects.get(username=self.valid_user["username"])
        user_hash = account_activation_token.generate_token(user)
        activation_link = "/auth/activate?hash=" + user_hash
        message = str(mail.outbox[0].body)
        send_to = mail.outbox[0].recipients()
        message_contains_activation_email = activation_link in message
        self.assertTrue(message_contains_activation_email)
        self.assertIn(user.email, send_to)

