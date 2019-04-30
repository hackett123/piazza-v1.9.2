from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Course
from django.contrib.auth.decorators import login_required

# Create your views here.


def splash(request):
    if request.user.is_authenticated:
        print(Course.objects.all())
        courses = [course for course in Course.objects.all() if request.user == course.instructor or request.user in course.students.all() or request.user in course.ta_staff.all()]
        return render(request, "home.html", {"user": request.user, "courses": courses})
    return render(request, "splash.html", {})

def login_(request):
    if request.method == "POST":
        print("LOGGING IN")
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
        if user is not None :
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
            email = request.POST['email'],
            username = request.POST['username'],
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            password = request.POST['password']
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
        course = Course.objects.create(
            name = request.POST['name'],
            term = request.POST['term'],
            code = request.POST['code'],
            instructor = request.user
        )
        return redirect("/course?course_id={course.id}")
    return render(request, 'create_course.html', {})

@login_required
def course(request):
    print(request.GET["course_id"]) 
    return redirect("/")