# Generated by Django 2.0.4 on 2018-04-24 00:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180424_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 0, 1, 41, 161969, tzinfo=utc)),
        ),
    ]
