# Generated by Django 3.2.25 on 2024-03-27 09:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20240327_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 27, 9, 23, 52, 155395, tzinfo=utc)),
        ),
    ]