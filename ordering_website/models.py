import random
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MaxLengthValidator

import uuid

import string


class Ranks(models.TextChoices):
    USER = "user"
    ADMIN = "admin"


class User(models.Model):
    user_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default='', max_length=255, null=True)
    surname = models.CharField(default='', max_length=255, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(unique=True, max_length=255)
    city = models.CharField(default='', max_length=255, null=True)
    registration_time = models.DateTimeField(auto_now_add=True)
    rank = models.CharField(max_length=20, choices=Ranks.choices, default=Ranks.USER)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,9}$",
        message="Phone number must be entered in the format: '999999999'.",
    )
    phone_number = models.CharField(default='', max_length=9, validators=[phone_regex], null=True)

    zip_regex = RegexValidator(
        regex=r"\d{2}-\d{3}",
        message="Zip code format must be in the format: XX-XXX.",
    )
    zip_code = models.CharField(default='', max_length=6, validators=[zip_regex], null=True)

    adress_regex = RegexValidator(
        regex=r"^[a-zA-Z]+?\s\w+$",
        message="Adress and number must be in the format: Street 1.",
    )

    address_and_number = models.CharField(default='', max_length=255, validators=[adress_regex], null=True)

    def __str__(self):
        if self.name is None or self.surname is None:
            return "Gość" + str(self.user_uid)
        return self.name + "_" + self.surname


class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(1000)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    producer = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    strain = models.CharField(max_length=100)
    aroma = models.CharField(max_length=100)
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    vol = models.DecimalField(max_digits=3, decimal_places=1)
    size = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    image = models.ImageField(upload_to='wines')

    def __str__(self):
        return self.name


class Rating(models.Model):
    rate_id = models.AutoField(primary_key=True)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(validators=[MaxLengthValidator(500)])

    def __str__(self):
        return self.rate_id


class PaymentMethods(models.TextChoices):
    TRANSFER = "transfer"
    PAYPAL = "paypal"


class DeliveryMethods(models.TextChoices):
    COURIER = "courier"
    PARCEL_LOCKER = "parcel_locker"


class OrderStatus(models.TextChoices):
    ORDERED = "ordered"
    PAID = "paid"
    SENT = "sent"
    DELIVERED = "delivered"


class OrderData(models.Model):
    order_id = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)

    name = models.CharField(default='', max_length=255)
    surname = models.CharField(default='', max_length=255)
    email = models.CharField(default='', max_length=255)
    city = models.CharField(default='', max_length=255)

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,9}$",
        message="Phone number must be entered in the format: '999999999'.",
    )
    phone_number = models.CharField(default='', max_length=9, validators=[phone_regex])

    zip_regex = RegexValidator(
        regex=r"\d{2}-\d{3}",
        message="Zip code format must be in the format: XX-XXX.",
    )
    zip_code = models.CharField(default='', max_length=6, validators=[zip_regex])

    adress_regex = RegexValidator(
        regex=r"^[a-zA-Z]+?\s\w+$",
        message="Adress and number must be in the format: Name Number.",
    )

    address_and_number = models.CharField(default='', validators=[adress_regex], max_length=255)

    payment = models.CharField(max_length=20, choices=PaymentMethods.choices, default=PaymentMethods.TRANSFER)
    delivery = models.CharField(max_length=20, choices=DeliveryMethods.choices, default=DeliveryMethods.COURIER)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.ORDERED)

    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        while not self.order_id:
            random_array = [
                random.sample(string.ascii_letters, 2),
                random.sample(string.digits, 2),
                random.sample(string.ascii_letters, 2),
            ]
            new_order_id = ''.join(item for innerlist in random_array for item in innerlist)

            if not OrderData.objects.filter(pk=new_order_id).exists():
                self.order_id = new_order_id

        super().save(*args, **kwargs)


class OrderedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderData, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
