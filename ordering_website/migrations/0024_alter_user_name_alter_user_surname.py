# Generated by Django 4.0.2 on 2022-12-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_website', '0023_alter_rating_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]