from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from RESTAuth.auth import UserRegistrationHandler, activate_user
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

    # def test_when_sign_up_user_then_not_active(self):
    #     reg = UserRegistrationHandler(self.valid_user)
    #     reg.sign_up()
    #     user = User.objects.get(username=self.valid_user.get("username"))
    #     self.assertFalse(user.is_active)

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

    # def test_if_activation_token_is_valid_then_activation_success(self):
    #     reg = UserRegistrationHandler(self.valid_user)
    #     reg.sign_up()
    #     user = User.objects.get(username=self.valid_user["username"])
    #     user_hash = account_activation_token.generate_token(user)
    #     success = activate_user(user_hash)
    #     self.assertTrue(success)

    # def test_send_not_success_when_activation_token_is_not_valid(self):
    #     success = activate_user("12kSAd212312pö97")
    #     self.assertFalse(success)

    # def test_user_is_active_after_activation(self):
    #     reg = UserRegistrationHandler(self.valid_user)
    #     reg.sign_up()
    #     user = User.objects.get(username=self.valid_user["username"])
    #     user_hash = account_activation_token.generate_token(user)
    #     activate_user(user_hash)
    #     user = User.objects.get(username=self.valid_user["username"])
    #     self.assertTrue(user.is_active)

    def test_when_user_is_sign_up_then_generate_auth_token(self):
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user["username"])
        self.assertIsNotNone(Token.objects.get(user=user))
