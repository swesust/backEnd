# Generated by Django 2.1.2 on 2019-01-22 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0005_post_time_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='time_data',
            new_name='time_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='time',
        ),
    ]