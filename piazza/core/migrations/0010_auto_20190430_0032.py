# Generated by Django 2.2 on 2019-04-30 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190429_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='number',
            field=models.CharField(default='COURSE NUMBER UNKNOWN', max_length=128),
        ),
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.CharField(default='COURSE TERM UNKNOWN', max_length=128),
        ),
    ]