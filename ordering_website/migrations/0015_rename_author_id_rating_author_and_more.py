# Generated by Django 4.0.2 on 2022-11-13 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering_website', '0014_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='wine_id',
            new_name='wine',
        ),
    ]