from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Post, Course, Followup
from django.contrib.auth.decorators import login_required

# Create your views here.


def splash(request):
    if request.user.is_authenticated:
        print(Course.objects.all())
        courses = [course for course in Course.objects.all() if request.user ==
                   course.instructor or request.user in course.students.all() or request.user in course.ta_staff.all()]
        return render(request, "home.html", {"user": request.user, "courses": courses})
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
        return redirect("/course?course_id="+str(course.id))
    return render(request, 'create_course.html', {"students": User.objects.all()})


@login_required
def course(request):
    course = Course.objects.get(id=request.GET["course_id"])
    return render(request, 'course.html', {"course": course, "user": request.user})


@login_required
def create_post(request):
    course = Course.objects.get(id=request.POST["course_id"])
    post = Post.objects.create(
        summary=request.POST["summary"],
        content=request.POST["content"],
        is_private=request.POST.get("post_to") == "private",
        author=request.user,
        course=course
    )
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
def view_post(request, course_id, post_id):
    post = Post.objects.get(id=post_id)
    course = Course.objects.get(id=course_id)
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
    return render(request, 'course.html', {"course": course, "post": post})


@login_required
def add_instructor_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    answer = request.POST.get("answer")

    post.instructor_answer = answer
    return render(request, 'course.html', {"course": course, "post": post})

@login_required
def add_student_answer(request):
    post_id = request.POST.get("post_id")
    post = Post.objects.get(id=post_id)

    course_id = request.POST.get("course_id")
    course = Course.objects.get(id=course_id)

    answer = request.POST.get("answer")

    post.student_answer = answer
    return render(request, 'course.html', {"course": course, "post": post})
