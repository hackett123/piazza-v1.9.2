from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def splash(request):
    return render(request, "splash.html", {})


def login_(request):
    if request.method == "POST":
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None :
            login(request, user)
            return redirect("/home")
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
        return redirect('/home')
    return render(request, 'signup.html', {})

def home(request):
    if request.user.is_authenticated :
        return render(request, "home.html", {"user":request.user})
    else :
        redirect("/")