# Generated by Django 3.0.4 on 2020-05-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schPortal', '0022_auto_20200506_1648'),
    ]

    operations = [
   
        migrations.AlterField(
            model_name='indexing',
            name='exam_sitting',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
