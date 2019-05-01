"""piazza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import splash, login_, signup_, logout_, create_course, course, create_post, render_post_form, delete_course, join_course, view_post, add_followup, add_instructor_answer, add_student_answer, folder, manage, update_course, edit_followup, edit_post, edit_instructor_answer, edit_student_answer

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", splash, name="splash"),
    path("login", login_, name="login"),
    path("signup", signup_, name="signup"),
    path("logout", logout_, name="logout"),
    path("create_course", create_course, name="create_course"),
    path("course", course, name="course"),
    path("create_post", create_post, name="create_post"),
    path("render_post_form", render_post_form, name="render_post_form"),
    path("delete_course", delete_course, name="delete_course"),
    path("join_course", join_course, name="join_course"),
    path("view_post", view_post, name="view_post"),
    path("add_followup", add_followup, name="add_followup"),
    path("add_instructor_answer", add_instructor_answer, name="add_instructor_answer"),
    path("add_student_answer", add_student_answer, name="add_student_answer"),
    path("folder", folder, name="folder"),
    path("manage", manage, name="manage"),
    path("update_course", update_course, name="update_course"),
    path("edit_followup", edit_followup, name="edit_followup"),
    path("edit_post", edit_post, name="edit_post"),
    path("edit_instructor_answer", edit_instructor_answer, name="edit_instructor_answer"),
    path("edit_student_answer", edit_student_answer, name="edit_student_answer")
]

