# Generated by Django 3.0.4 on 2020-05-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schPortal', '0025_auto_20200509_1236'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='examregistration',
            name='approved',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='examregistration',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='examregistration',
            name='declined',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]