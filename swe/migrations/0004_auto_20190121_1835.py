# Generated by Django 2.1.2 on 2019-01-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swe', '0003_auto_20190119_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='facebookid',
            field=models.CharField(default='home', max_length=30),
        ),
        migrations.AddField(
            model_name='student',
            name='twitterid',
            field=models.CharField(default='home', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='githubid',
            field=models.CharField(default='home', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='linkedinid',
            field=models.CharField(default='home', max_length=30),
        ),
    ]
