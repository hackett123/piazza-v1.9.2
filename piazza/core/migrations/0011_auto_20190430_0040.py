# Generated by Django 2.2 on 2019-04-30 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190430_0032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='number',
        ),
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(default='COURSE CODE UNKNOWN', max_length=128),
        ),
    ]
