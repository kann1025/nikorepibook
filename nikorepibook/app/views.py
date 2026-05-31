from django.shortcuts import render
from .models import Recipe

# Create your views here.

from django.http import HttpResponse

def home(request):
    recipes = Recipe.objects.all()
    return render(request,"app/home.html",{'recipes':recipes})

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

def calendar_add(request):
    return render(request,"app/calendar_add.html")

def recipi_create(request):
    return render(request,"app/recipe_create.html")

def mypage_edit(request):
    return render(request,"app/mypage_edit.html")