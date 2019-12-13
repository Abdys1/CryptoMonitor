from django.db import models


class RegistrationMessage(models.Model):
    success = models.BooleanField

    def __init__(self, success):
        self.success = success

    class Meta:
        managed = False
