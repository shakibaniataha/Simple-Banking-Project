# Generated by Django 3.2.7 on 2021-09-13 13:24

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_baseusermodel_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseusermodel',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=255, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()]),
        ),
    ]
