from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    return render(request,"app/home.html")

def login_view(request):
    return render(request,"app/login.html")

def signup_view(request):
    return render(request,"app/signup.html")

def recipe_detail(request):
    return render(
        request,
        "app/recipe_detail.html"
    )
    
def shoppinng_list(request):
    return render(request,"app/shopping_list.html")

def calendar_view(request):
    return render(request, "app/calendar.html")

def mypage(request):
    return render(request, "app/mypage.html")