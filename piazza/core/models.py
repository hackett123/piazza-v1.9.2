from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=128, default="COURSE NAME UNKNOWN")
    code = models.CharField(max_length=128, default="COURSE CODE UNKNOWN")
    term = models.CharField(max_length=128, default="COURSE TERM UNKNOWN")
    instructor = models.ForeignKey(User, related_name="instructor_courses", on_delete=models.CASCADE, default=0)
    students = models.ManyToManyField(User, related_name="student_courses", default=0)
    ta_staff = models.ManyToManyField(User, related_name="TA_courses", default=0)

    def __str__(self):
        return self.code + ": " + self.name +"[" + self.term + "]"

class Folder(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=128, default="FOLDER NAME UNKNOWN")
    course = models.ForeignKey(Course, related_name="course_folders", on_delete=models.CASCADE, default=0)

class Post(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=128)
    content = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author", default="NULL")
    is_question = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    good_questions = models.IntegerField(default=0)
    folder = models.ManyToManyField(Folder, related_name ="folder_posts", default=0)
    course = models.ForeignKey(Course, related_name="course_posts", on_delete=models.CASCADE, default=0)
    instructor_answer = models.TextField(default="")
    student_answer = models.TextField(default="")
    
    def __str__(self):
        return self.author.username + " posted : " + self.summary
    
    def __dir__(self):
        return "id, created_at, summary, content, author, is_question, is_private, good_questions, folder, course, instructor_answer, student_answer"


    # def __getattr__(self, name):
    #     return name

class Followup(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_followups")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_followups", default=0)

    
    

