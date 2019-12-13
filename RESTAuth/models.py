from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework.exceptions import ValidationError


class RegistrationMessage(models.Model):
    success = models.BooleanField

    def __init__(self, success):
        self.success = success

    class Meta:
        managed = False