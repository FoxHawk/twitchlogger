# Generated by Django 3.2.7 on 2021-11-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitchEvents', '0002_auto_20211002_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='eventID',
            field=models.CharField(max_length=40),
        ),
    ]