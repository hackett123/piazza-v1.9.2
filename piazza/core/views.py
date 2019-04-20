from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import Course

# Create your views here.


def splash(request):
    return render(request, "splash.html", {})


def login_(request):
    if request.method == "POST":
        print("LOGGING IN")
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
        if user is not None :
            print("LOGGED IN")
            login(request, user)
            return redirect("/home")
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
        return redirect('/home')
    return render(request, 'signup.html', {})

def home(request):
    if request.user.is_authenticated :
        courses = [course for course in Course.objects.all() if request.user in course]
        return render(request, "home.html", {"user":request.user, "courses":courses})
    else :
        redirect("/")