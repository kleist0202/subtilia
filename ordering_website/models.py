from django.db import models
from django.core.validators import RegexValidator

import uuid


class Ranks(models.TextChoices):
    USER = "user"
    ADMIN = "admin"


class User(models.Model):
    user_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    surname = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(unique=True, max_length=255)
    city = models.CharField(max_length=255)
    registration_time = models.DateTimeField(auto_now_add=True)
    rank = models.CharField(max_length=20, choices=Ranks.choices, default=Ranks.USER)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,9}$",
        message="Phone number must be entered in the format: '+999999999'.",
    )
    phone_number = models.CharField(max_length=9, validators=[phone_regex])

    zip_regex = RegexValidator(
        regex=r"^\d{2}(?:[-\s]\d{3})?$",
        message="Zip code format must be in the format: XX-XXX or XXXXX or XX XXX.",
    )
    zip_code = models.CharField(max_length=6, validators=[zip_regex])

    address_and_number = models.CharField(max_length=255)

    def __str__(self):
        return self.username
