# Generated by Django 2.1.2 on 2019-01-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0007_auto_20190122_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imgsrc',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
