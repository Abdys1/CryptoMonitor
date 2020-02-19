from django.contrib.auth.models import User
from django.test import TestCase

from .auth import UserRegistrationHandler
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegistrationTest(TestCase):
    def setUp(self) -> None:
        self.valid_user = {"username": "User", "email": "example@gmail.com", "password": "1221313"}
        self.invalid_user = {"username": "User2", "email": "", "password": "1221313"}

    def test_can_sign_up(self) -> None:
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        self.assertIsNotNone(success)

    def test_when_sign_up_is_success_then_send_true(self) -> None:
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        self.assertTrue(success)

    def test_when_user_try_sign_up_with_invalid_data_then_send_false(self) -> None:
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)

    def test_when_user_try_sign_up_with_invalid_data_then_has_error_message(self) -> None:
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertIsNotNone(reg.errors)

    def test_when_user_try_sign_up_with_short_username_then_send_username_error(self) -> None:
        self.invalid_user["username"] = "asd"
        self.invalid_user["email"] = "example@example.com"
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["username"][0], "Túl rövid felhasználónév!")

    def test_when_user_try_sign_up_without_email_then_send_email_error(self) -> None:
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["email"][0], "Adjon meg egy email címet!")

    def test_when_try_sign_up_with_wrong_email_then_send_email_error(self) -> None:
        self.invalid_user["email"] = "dsadadsad.com"
        reg = UserRegistrationHandler(self.invalid_user)
        success = reg.sign_up()
        self.assertFalse(success)
        self.assertEqual(reg.errors["email"][0], "Adjon meg egy érvényes e-mail címet!")

    def test_save_valid_user_to_database(self) -> None:
        reg = UserRegistrationHandler(self.valid_user)
        success = reg.sign_up()
        user = User.objects.get(username=self.valid_user.get("username"))
        self.assertTrue(success)
        self.assertIsNotNone(user)

    def test_try_sign_up_two_same_username(self) -> None:
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.assertEqual(reg.errors["username"][0], "Létezik már egy felhasználó ezzel a névvel.")

    def test_try_sign_up_with_same_email_then_send_error(self) -> None:
        self.valid_user["username"] = "User1"
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.valid_user["username"] = "User2"
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        self.assertEqual(reg.errors["email"][0], "Létezik már egy felhasználó ezzel az e-mail címmel!")

    def test_when_user_is_sign_up_then_generate_auth_token(self) -> None:
        reg = UserRegistrationHandler(self.valid_user)
        reg.sign_up()
        user = User.objects.get(username=self.valid_user["username"])
        self.assertIsNotNone(Token.objects.get(user=user))


class AccountInformationTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="User", password="1234567", email="example@gmail.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))

    def test_has_OK_response_when_get_account_information(self) -> None:
        response = self.client.get("/auth/account")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_has_account_info_in_response(self) -> None:
        response = self.client.get("/auth/account")
        self.assertIsNotNone(response.data)
        self.assertTrue("id" in response.data)
        self.assertTrue("username" in response.data)
        self.assertTrue("email" in response.data)

    def test_account_infos_agree(self) -> None:
        response = self.client.get("/auth/account")
        self.assertEqual(self.user.pk, response.data.get("id"))
        self.assertEqual(self.user.username, response.data.get("username"))
        self.assertEqual(self.user.email, response.data.get("email"))

    def test_cannot_get_infos_when_not_authorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get("/auth/account")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)