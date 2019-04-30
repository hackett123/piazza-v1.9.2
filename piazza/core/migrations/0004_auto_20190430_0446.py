# Generated by Django 2.2 on 2019-04-30 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190430_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='instructor_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(default=0, related_name='student_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='ta_staff',
            field=models.ManyToManyField(default=0, related_name='TA_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_followups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='followup',
            name='post',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='post_followups', to='core.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='course',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='course_posts', to='core.Course'),
        ),
        migrations.AlterField(
            model_name='post',
            name='folder',
            field=models.ManyToManyField(default=0, related_name='folder_posts', to='core.Folder'),
        ),
    ]
