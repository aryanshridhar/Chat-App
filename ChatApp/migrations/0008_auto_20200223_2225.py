# Generated by Django 2.2.7 on 2020-02-23 16:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0007_chat_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 23, 16, 55, 17, 366206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currentchat',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]
