# Generated by Django 3.2.7 on 2022-02-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitchEvents', '0007_logentry_eventid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelEvents',
            fields=[
                ('channel', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('streamUp', models.BooleanField(default=True)),
                ('streamDown', models.BooleanField(default=True)),
                ('streamUpdate', models.BooleanField(default=True)),
            ],
        ),
    ]
