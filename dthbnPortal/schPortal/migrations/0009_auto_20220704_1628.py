# Generated by Django 3.0 on 2022-07-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schPortal', '0008_auto_20220704_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examregistration',
            name='lga_of_origin',
        ),
        migrations.AlterField(
            model_name='examregistration',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
