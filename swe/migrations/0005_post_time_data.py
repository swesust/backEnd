# Generated by Django 2.1.2 on 2019-01-22 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0004_auto_20190121_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time_data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]