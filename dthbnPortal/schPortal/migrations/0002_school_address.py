# Generated by Django 3.0.4 on 2020-04-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schPortal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
