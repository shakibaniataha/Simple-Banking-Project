# Generated by Django 3.2.7 on 2021-09-13 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_baseusermodel_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseusermodel',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
