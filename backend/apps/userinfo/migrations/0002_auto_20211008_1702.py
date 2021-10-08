# Generated by Django 3.2.7 on 2021-10-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='location_lat',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='location_lon',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_bio',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
