from django.db import models
from django.core.validators import RegexValidator

import uuid


class Ranks(models.TextChoices):
    USER = "user"
    ADMIN = "admin"


class User(models.Model):
    user_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255, null=True)
    surname = models.CharField(unique=True, max_length=255, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(unique=True, max_length=255)
    city = models.CharField(max_length=255, null=True)
    registration_time = models.DateTimeField(auto_now_add=True)
    rank = models.CharField(max_length=20, choices=Ranks.choices, default=Ranks.USER)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,9}$",
        message="Phone number must be entered in the format: '+999999999'.",
    )
    phone_number = models.CharField(max_length=9, validators=[phone_regex], null=True)

    zip_regex = RegexValidator(
        # regex=r"^\d{2}(?:[-\s]\d{3})?$",
        regex=r"\d{2}-\d{3}",
        message="Zip code format must be in the format: XX-XXX.",
    )
    zip_code = models.CharField(max_length=6, validators=[zip_regex], null=True)

    address_and_number = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username


class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='wines')

    def __str__(self):
        return self.name
