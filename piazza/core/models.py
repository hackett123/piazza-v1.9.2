from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=3, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name, self.last_name

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    username = models.CharField(max_length=3, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name, self.last_name
    
class Followup(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followup_author")

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author", default="NULL")
    is_question = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    good_questions = models.IntegerField(default=0)
    followups = models.ManyToManyField(Followup, related_name="followups")

    def __str__(self):
        return self.author, " posted : ", self.content

class Folder(models.Model):
    pass

class Course(models.Model):
    pass
