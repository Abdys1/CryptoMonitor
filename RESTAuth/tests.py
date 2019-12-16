from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core import mail
from django.test import TestCase, RequestFactory

from RESTAuth.serializers import RegistrationSerializer
from RESTAuth.auth import sign_up, activate_user, login_user
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

    def test_if_activation_token_is_valid_then_activation_success(self):
        sign_up(self.valid_user)
        user = User.objects.get(username=self.valid_user["username"])
        user_hash = account_activation_token.generate_token(user)
        success = activate_user(user_hash)
        self.assertTrue(success)

    def test_send_not_success_when_activation_token_is_not_valid(self):
        success = activate_user("12kSAd212312pö97")
        self.assertFalse(success)

    def test_user_is_active_after_activation(self):
        sign_up(self.valid_user)
        user = User.objects.get(username=self.valid_user["username"])
        user_hash = account_activation_token.generate_token(user)
        activate_user(user_hash)
        user = User.objects.get(username=self.valid_user["username"])
        self.assertTrue(user.is_active)


class LoginTest(TestCase):
    def setUp(self):
        self.activated_user_data = {"username": "User", "email": "example@gmail.com", "password": "1221313"}
        sign_up(self.activated_user_data)
        username = self.activated_user_data.get("username")
        user = User.objects.get(username=username)
        user_hash = account_activation_token.generate_token(user)
        activate_user(user_hash)

        self.inactive_user_data = {"username": "User2", "email": "example2@gmail.com", "password": "jelszo12345"}
        sign_up(self.inactive_user_data)

        rf = RequestFactory()
        self.request = rf.post("/login")
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_has_login_message(self):
        login_message = login_user(self.request, self.activated_user_data.get("username"), self.activated_user_data.get("password"))
        self.assertIsNotNone(login_message)

    def test_when_the_user_exists_and_the_password_match_then_send_success_message(self):
        login_message = login_user(self.request, self.activated_user_data.get("username"), self.activated_user_data.get("password"))
        self.assertTrue(login_message.data["success"])

    def test_when_the_user_exists_and_the_password_not_match(self):
        login_message = login_user(self.request, self.activated_user_data.get("username"), self.inactive_user_data.get("password"))
        self.assertFalse(login_message.data["success"])

    def test_when_the_user_is_inactive_then_send_not_success(self):
        login_message = login_user(self.request, self.inactive_user_data.get("username"), self.inactive_user_data.get("password"))
        self.assertFalse(login_message.data["success"])

    def test_when_user_not_exists_send_not_success(self):
        login_message = login_user(self.request, "nemletezik", "ezsem")
        self.assertFalse(login_message.data["success"])

    def test_when_login_is_success_then_send_username(self):
        login_message = login_user(self.request, self.activated_user_data.get("username"), self.activated_user_data.get("password"))
        self.assertEqual(login_message.data["username"], self.activated_user_data.get("username"))

    def test_when_login_is_success_add_session_for_user(self):
        login_user(self.request, self.activated_user_data.get("username"), self.activated_user_data.get("password"))
        user = auth.get_user(self.request)
        self.assertTrue(user.is_authenticated)