# Generated by Django 3.2.7 on 2021-12-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitchEvents', '0005_auto_20211204_1510'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UpdateLogEntry',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='startedAt',
            new_name='datetimestamp',
        ),
        migrations.AddField(
            model_name='logentry',
            name='type',
            field=models.CharField(default='stream.online', max_length=20),
            preserve_default=False,
        ),
    ]
