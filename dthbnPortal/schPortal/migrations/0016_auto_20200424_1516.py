# Generated by Django 3.0.4 on 2020-04-24 15:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('schPortal', '0015_auto_20200424_1450'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='school',
            name='updated_at',
            field=models.DateField(default=datetime.datetime(2020, 4, 24, 15, 15, 59, 759458, tzinfo=utc)),
        ),
    ]
