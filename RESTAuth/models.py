from django.db import models


class RegistrationMessage(models.Model):
    success = models.BooleanField

    def __init__(self, success):
        self.success = success

    class Meta:
        managed = False


class LoginMessage(models.Model):
    success = models.BooleanField
    username = models.CharField

    def __init__(self, success, username):
        self.success = success
        self.username = username

    class Meta:
        managed = False