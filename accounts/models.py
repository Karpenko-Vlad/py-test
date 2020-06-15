from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    phone_number = models.CharField(max_length=15, null=True)

    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=75, null=True)

    postcode = models.CharField(max_length=10, null=True)
