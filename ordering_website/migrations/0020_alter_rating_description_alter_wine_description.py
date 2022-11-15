# Generated by Django 4.0.2 on 2022-11-15 15:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_website', '0019_alter_wine_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='description',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(500)]),
        ),
        migrations.AlterField(
            model_name='wine',
            name='description',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(1000)]),
        ),
    ]