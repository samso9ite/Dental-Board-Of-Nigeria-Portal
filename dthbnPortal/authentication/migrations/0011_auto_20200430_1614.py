# Generated by Django 3.0.4 on 2020-04-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='block',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='suspend',
            field=models.BooleanField(default=False),
        ),
    ]
