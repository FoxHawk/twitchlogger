# Generated by Django 3.2.7 on 2021-10-02 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitchEvents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='channel',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='eventEntry',
        ),
    ]
