# Generated by Django 3.2.7 on 2021-09-13 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210913_1102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseusermodel',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]