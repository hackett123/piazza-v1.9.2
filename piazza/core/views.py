from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Post, Course, Followup, Folder
from django.contrib.auth.decorators import login_required

import csv, time
from django.http import HttpResponse


def splash(request):
    if request.user.is_authenticated:
        print(Course.objects.all())
        ta_course_ids = request.user.TA_courses.all()
        ta_courses = Course.objects.filter(id__in=ta_course_ids)

        instructor_course_ids = request.user.instructor_courses.all()
        instructor_courses = Course.objects.filter(id__in=instructor_course_ids)

        student_course_ids = request.user.student_courses.all()
        student_courses = Course.objects.filter(id__in=student_course_ids)
        # courses = [course for course in Course.objects.all() if request.user ==
        #            course.instructor or request.user in course.students.all() or request.user in course.ta_staff.all()]
        return render(request, "home.html", {"user": request.user, "ta_courses": ta_courses, "instructor_courses": instructor_courses, "student_courses": student_courses})
    return render(request, "splash.html", {})


def login_(request):
    if request.method == "POST":
        print("LOGGING IN")
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        print(user)
        if user is not None:
            print("LOGGED IN")
            login(request, user)
            return redirect("/")
        print("COULD NOT FIND USER")
    return render(request, "login.html", {})


def logout_(request):
    logout(request)
    return redirect("/")


def signup_(request):
    if request.method == "POST":
        user = User.objects.create_user(
            email=request.POST['email'],
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            password=request.POST['password']
        )
        login(request, user)
        print("CREATED USER")
        print(request.POST['email'])
        print(request.POST['password'])
        return redirect('/')
    return render(request, 'signup.html', {})


@login_required
def create_course(request):
    if request.method == "POST":
        # https://stackoverflow.com/questions/618557/django-using-select-multiple-and-post
        student_ids = request.POST.getlist("students")
        ta_ids = request.POST.getlist("tas")
        # https://stackoverflow.com/questions/6337973/get-multiple-rows-with-one-query-in-django
        students = User.objects.filter(id__in=student_ids)
        tas = User.objects.filter(id__in=ta_ids)

        course = Course.objects.create(
            name=request.POST['name'],
            term=request.POST['term'],
            code=request.POST['code'],
            instructor=request.user
        )
        for student in students:
            print("STUDENT : ", student.first_name)
        for ta in tas:
            print("TA : ", ta.first_name)
        print("Instructor : ", course.instructor)
        course.students.set(students)
        course.ta_staff.set(tas)

        folder_string = request.POST['folders']
        folders = folder_string.split(",")
        folders = list(map(lambda x: x.strip(), folders))
        for f in folders:
            Folder.objects.create(
                name=f,
                course=course
            )
        return redirect("/course?course_id="+str(course.id))
    return render(request, 'create_course.html', {"students": User.objects.all()})


@login_required
def course(request):
    course = Course.objects.get(id=request.GET["course_id"])
    return render(request, 'course.html', {"course": course, "user": request.user})


@login_required
def create_post(request):
    course = Course.objects.get(id=request.POST["course_id"])
    folder_ids = request.POST.getlist("folders")
    folders = Folder.objects.filter(id__in=folder_ids)
    post = Post.objects.create(
        summary=request.POST["summary"],
        content=request.POST["content"],
        is_private=request.POST.get("post_to") == "private",
        author=request.user,
        course=course,
        is_question=request.POST.get("post_type") == "question"
    )
    post.folder.set(folders)
    return redirect("/course?course_id="+str(course.id))


@login_required
def render_post_form(request):
    course = Course.objects.get(id=request.POST["course_id"])
    return render(request, 'course.html', {"course": course, "create": True})


@login_required
def delete_course(request):
    print(request.GET.get("course_id"))
    course = Course.objects.get(id=request.GET.get('course_id'))
    print("PRINTING COURSE : ", course)
    course.delete()
    return redirect('/')


@login_required
def join_course(request):
    if request.method == "POST":
        course_ids = request.POST.getlist("courses")
        user = request.user
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            course.students.add(user)
        return redirect("/")
    id = request.user.id
    courses = Course.objects.exclude(students__id=id)
    return render(request, "join_course.html", {"courses": courses})


@login_required
def view_post(request):
    course_id = request.GET.get("course_id")
    course = Course.objects.get(id=course_id)

    post_id = request.GET.get("post_id")
    post = course.course_posts.get(id=post_id)

    return render(request, 'course.html', {"course": course, "post": post})


@login_required
def add_followup(request):
    content = request.POST.get("followup")
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)
    followup = Followup.objects.create(
        content=content,
        author=request.user,
        post=post
    )
    return redirect("/view_post?course_id="+str(course.id)+"&post_id="+str(post.id))


@login_required
def add_instructor_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    answer = request.POST.get("answer")

    post.instructor_answer = answer
    post.save()
    return render(request, 'course.html', {"course": course, "post": post})


@login_required
def add_student_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    answer = request.POST.get("answer")

    post.student_answer = answer
    post.save()
    return render(request, 'course.html', {"course": course, "post": post})


@login_required
def folder(request):
    folder_id = request.GET.get("folder_id")
    folder = Folder.objects.get(id=folder_id)

    course_id = request.GET.get("course_id")
    course = Course.objects.get(id=course_id)

    posts = course.course_posts.filter(folder=folder)

    return render(request, 'course.html', {"course": course, "filter": True, "posts": posts})


@login_required
def manage(request):
    course = Course.objects.get(id=request.GET["course_id"])
    # curr_tas/students, new_tas/students, folder_string
    if request.user == course.instructor:
        new_tas = User.objects.exclude(id__in=course.ta_staff.all())
        new_students = User.objects.exclude(id__in=course.students.all())

        folder_string = ""
        for f in course.course_folders.all():
            folder_string = folder_string + f.name + ", "
        folder_string = folder_string[:len(folder_string)-2]
        return render(request, 'manage.html', {"course": course, "curr_students": course.students.all(),
                                               "curr_tas": course.ta_staff.all(), "new_tas": new_tas, "new_students": new_students, "folder_string": folder_string})
    return redirect("/")


@login_required
def update_course(request):
    course = Course.objects.get(id=request.POST.get("course_id"))
    add_students = User.objects.filter(
        id__in=request.POST.getlist("add_students"))
    add_tas = User.objects.filter(id__in=request.POST.getlist("add_tas"))
    remove_students = User.objects.filter(
        id__in=request.POST.getlist("remove_students"))
    remove_tas = User.objects.filter(id__in=request.POST.getlist("remove_tas"))
    remove_folders = Folder.objects.filter(
        id__in=request.POST.getlist("remove_folders"))

    for student in remove_students:
        course.students.remove(student)
<<<<<<< HEAD

    for ta in remove_tas:
        course.ta_staff.remove(ta)
=======
        #student.delete()

    for ta in remove_tas:
        course.ta_staff.remove(ta)
        #ta.delete()
>>>>>>> b2e3f9c0cc96adf33772333e00c79f0806cf3b6f

    for folder in remove_folders:
        folder.delete()

    for student in add_students:
        course.students.add(student)

    for ta in add_tas:
        course.ta_staff.add(ta)

    course.name = request.POST['name']
    course.term = request.POST['term']
    course.code = request.POST['code']

    folder_string = request.POST['add_folders']
    if len(folder_string) > 0:
        folders = folder_string.split(",")
        folders = list(map(lambda x: x.strip(), folders))
        for f in folders:
            Folder.objects.create(
                name=f,
                course=course
            )

    course.save()
    return redirect("/course?course_id="+str(course.id))


@login_required
def edit_followup(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    content = request.POST.get("followup")
    followup_id = request.POST.get("followup_id")

    followup = post.post_followups.get(id=followup_id)
    followup.content = content
    followup.save()
    return redirect("/view_post?course_id="+str(course.id)+"&post_id="+str(post.id))

@login_required
def edit_post(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    content = request.POST.get("content")

    post.content = content
    post.save()
    return redirect("/view_post?course_id="+str(course.id)+"&post_id="+str(post.id))

@login_required
def edit_instructor_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    content = request.POST.get("content")

    post.instructor_answer = content
    post.save()
    return redirect("/view_post?course_id="+str(course.id)+"&post_id="+str(post.id))

@login_required
def edit_student_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    content = request.POST.get("content")

    post.student_answer = content
    post.save()
    return redirect("/view_post?course_id="+str(course.id)+"&post_id="+str(post.id))

#credit to https://docs.djangoproject.com/en/2.2/howto/outputting-csv/ for help
@login_required
def export_course(request):
    course = Course.objects.get(id=request.GET.get("course_id"))
    students = course.students.all()
    tas = course.ta_staff.all()
    posts = course.course_posts.all()

    
    response = HttpResponse(content_type='text/csv')

    # https://www.tutorialspoint.com/python/python_date_time.htm
    t = str(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
    response['Content-Disposition'] = 'attachment; filename='+str(course)+'_'+t+'.csv'
    writer = csv.writer(response)

    writer.writerow(["Student First Name", "Student Last Name", "Student Username", "Student Email"])
    for student in students:
        writer.writerow([student.first_name,student.last_name,student.username,student.email])

    writer.writerow(["TA First Name", "TA Last Name", "TA Username", "TA Email"])
    for ta in students:
        writer.writerow([ta.first_name,ta.last_name,ta.username,ta.email])
    
    writer.writerow(["Post Author", "Post Date", "Post Summary", "Post Content", "Post Privacy", "Instructor Answer", "Student Answer"])
    for post in posts:
        writer.writerow([post.author,post.created_at,post.summary,post.content,post.is_private,post.instructor_answer,post.student_answer])
    
    return response