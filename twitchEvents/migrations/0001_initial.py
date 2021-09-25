# Generated by Django 3.2.7 on 2021-09-25 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='eventEntry',
            fields=[
                ('id', models.CharField(max_length=30)),
                ('channel', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startedAt', models.DateTimeField()),
                ('eventID', models.IntegerField()),
                ('type', models.CharField(max_length=20)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitchEvents.evententry')),
            ],
        ),
    ]
