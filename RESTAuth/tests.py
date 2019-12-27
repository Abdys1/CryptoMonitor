from django.contrib import auth
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, RequestFactory

from RESTAuth.auth import UserRegistrationHandler, activate_user
from RESTAuth.tokens import account_activation_token
from rest_framework.authtoken.models import Token


class RegistrationTest(TestCase):
    def setUp(self):
        self.valid_user = {"username": "User", "email": "example@gmail.com", "password": "1221313"}
        self.invalid_user = {"username": "User2", "email": "", "password": "1221313"}

    def test_can_sign_up(self):
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        self.assertIsNotNone(success)

    def test_when_sign_up_is_success_then_send_true(self):
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        self.assertTrue(success)

    def test_when_user_try_sign_up_with_invalid_data_then_send_false(self):
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)

    def test_when_user_try_sign_up_with_invalid_data_then_has_error_message(self):
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertIsNotNone(reg.errors)

    def test_when_user_try_sign_up_with_short_username_then_send_username_error(self):
        self.invalid_user["username"] = "asd"
        self.invalid_user["email"] = "example@example.com"
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["username"][0], "Túl rövid felhasználónév!")

    def test_when_user_try_sign_up_without_email_then_send_email_error(self):
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["email"][0], "Adjon meg egy email címet!")

    def test_when_try_sign_up_with_wrong_email_then_send_email_error(self):
        self.invalid_user["email"] = "dsadadsad.com"
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["email"][0], "Adjon meg egy érvényes e-mail címet!")

    def test_save_valid_user_to_database(self):
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        user = User.objects.get(username=self.valid_user.get("username"))
        self.assertTrue(success)
        self.assertIsNotNone(user)

    def test_when_sign_up_user_then_not_active(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user.get("username"))
        self.assertFalse(user.is_active)

    def test_try_sign_up_two_same_username(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.assertEqual(reg.errors["username"][0], "Létezik már egy felhasználó ezzel a névvel.")

    def test_try_sign_up_with_same_email_then_send_error(self):
        self.valid_user["username"] = "User1"
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.valid_user["username"] = "User2"
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.assertEqual(reg.errors["email"][0], "Létezik már egy felhasználó ezzel az e-mail címmel!")

    # def test_send_to_user_activate_email(self):
    #     reg = UserRegistrationHandler(self.valid_user)
    #     reg.sign_up()
    #     user = User.objects.get(username=self.valid_user["username"])
    #     user_hash = account_activation_token.generate_token(user)
    #     activation_link = "/auth/activate?hash=" + user_hash
    #     message = str(mail.outbox[0].body)
    #     send_to = mail.outbox[0].recipients()
    #     message_contains_activation_email = activation_link in message
    #     self.assertTrue(message_contains_activation_email)
    #     self.assertIn(user.email, send_to)

    def test_if_activation_token_is_valid_then_activation_success(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user["username"])
        user_hash = account_activation_token.generate_token(user)
        success = activate_user(user_hash)
        self.assertTrue(success)

    def test_send_not_success_when_activation_token_is_not_valid(self):
        success = activate_user("12kSAd212312pö97")
        self.assertFalse(success)

    def test_user_is_active_after_activation(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user["username"])
        user_hash = account_activation_token.generate_token(user)
        activate_user(user_hash)
        user = User.objects.get(username=self.valid_user["username"])
        self.assertTrue(user.is_active)

    def test_when_user_is_sign_up_then_generate_auth_token(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user["username"])
        print(Token.objects.get(user=user))
        self.assertIsNotNone(Token.objects.get(user=user))
#
# class LoginTest(TestCase):
#     def setUp(self):
#         self.activated_user_data = {"username": "User", "email": "example@gmail.com", "password": "1221313"}
#         reg = UserRegistrationHandler(self.activated_user_data)
#         reg.sign_up()
#         username = self.activated_user_data.get("username")
#         user = User.objects.get(username=username)
#         user_hash = account_activation_token.generate_token(user)
#         activate_user(user_hash)
#
#         self.inactive_user_data = {"username": "User2", "email": "example2@gmail.com", "password": "jelszo12345"}
#         reg = UserRegistrationHandler(self.inactive_user_data)
#         reg.sign_up()
#
#         rf = RequestFactory()
#         self.request = rf.post("/login")
#         middleware = SessionMiddleware()
#         middleware.process_request(self.request)
#         self.request.session.save()
#
#         self.loginHandler = UserLoginHandler(self.request)
#
#     def test_when_the_user_exists_and_the_password_match_then_send_success_message(self):
#         success = self.loginHandler.login_user(self.activated_user_data.get("username"), self.activated_user_data.get("password"))
#         self.assertTrue(success)
#
#     def test_when_the_user_exists_and_the_password_not_match(self):
#         success = self.loginHandler.login_user(self.activated_user_data.get("username"), self.inactive_user_data.get("password"))
#         self.assertFalse(success)
#
#     def test_when_the_user_is_inactive_then_send_not_success(self):
#         success = self.loginHandler.login_user(self.inactive_user_data.get("username"), self.inactive_user_data.get("password"))
#         self.assertFalse(success)
#
#     def test_when_user_not_exists_send_error(self):
#         self.loginHandler.login_user("nemletezik", "ezsem")
#         self.assertEqual(self.loginHandler.messages["error"], "Helytelen belépési adatok!")
#
#     def test_when_login_is_success_then_send_username(self):
#         self.loginHandler.login_user(self.activated_user_data.get("username"), self.activated_user_data.get("password"))
#         self.assertEqual(self.loginHandler.messages["username"], self.activated_user_data.get("username"))
#
#     def test_when_login_is_success_add_session_for_user(self):
#         self.loginHandler.login_user(self.activated_user_data.get("username"), self.activated_user_data.get("password"))
#         user = auth.get_user(self.request)
#         self.assertTrue(user.is_authenticated)
