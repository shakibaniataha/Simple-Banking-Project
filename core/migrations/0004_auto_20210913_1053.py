# Generated by Django 3.2.7 on 2021-09-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_baseusermodel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseusermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='baseusermodel',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
