# Generated by Django 4.0.2 on 2022-11-01 22:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_website', '0004_alter_user_address_and_number_alter_user_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('wine_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Zip code format must be in the format: XX-XXX.', regex='\\d{2}-\\d{3}')]),
        ),
    ]
