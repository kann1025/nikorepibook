from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    return render(request,"app/home.html")

def login_view(request):
    return render(request,"app/login.html")

def signup_view(request):
    return render(request,"app/signup.html")