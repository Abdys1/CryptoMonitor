from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from authenticate.service import RegistrationHandler
from authenticate.serializer import RegistrationSerializer


class RegistrationTest(TestCase):
    def setUp(self):
        self.reg_handler = RegistrationHandler()
        self.valid_user = User.objects.create_user('User1', 'example@gmail.com', '1234567')
        self.invalid_user = User.objects.create_user('User2', '', '21312')

    def test_has_reg_message(self):
        reg_message = self.reg_handler.registrate(self.valid_user)
        self.assertIsNotNone(reg_message)

    def test_message_is_serialized(self):
        reg_message = self.reg_handler.registrate(self.valid_user)
        is_reg_serializer = isinstance(reg_message, RegistrationSerializer)
        self.assertTrue(is_reg_serializer)

    def test_send_success_message_when_registration_is_valid(self):
        reg_message = self.reg_handler.registrate(self.valid_user)
        self.assertTrue(reg_message.data["success"])

    def test_send_not_success_message_when_user_has_not_mail(self):
        reg_message = self.reg_handler.registrate(self.invalid_user)
        self.assertFalse(reg_message.data["success"])

    def test_send_not_success_message_when_user_has_not_username(self):
        self.invalid_user.username = ""
        self.invalid_user.email = "example2@gmail.com"
        reg_message = self.reg_handler.registrate(self.invalid_user)
        self.assertFalse(reg_message.data["success"])