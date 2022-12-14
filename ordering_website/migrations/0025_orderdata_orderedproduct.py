# Generated by Django 4.0.2 on 2022-12-02 22:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_website', '0024_alter_user_name_alter_user_surname'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('order_id', models.SlugField(blank=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=255, null=True)),
                ('surname', models.CharField(default='', max_length=255, null=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('city', models.CharField(default='', max_length=255, null=True)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('rank', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=20)),
                ('phone_number', models.CharField(default='', max_length=9, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'.", regex='^\\+?1?\\d{9,9}$')])),
                ('zip_code', models.CharField(default='', max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Zip code format must be in the format: XX-XXX.', regex='\\d{2}-\\d{3}')])),
                ('address_and_number', models.CharField(default='', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering_website.orderdata')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering_website.wine')),
            ],
        ),
    ]