# Generated by Django 2.1.7 on 2019-04-19 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_course_ta_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='name',
            field=models.CharField(default='FOLDER NAME UNKNOWN', max_length=128),
        ),
        migrations.AlterField(
            model_name='folder',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]