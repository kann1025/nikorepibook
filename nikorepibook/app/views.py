from django.shortcuts import render,redirect
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

def recipe_detail(request,recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(
        request,
        "app/recipe_detail.html",
        {"recipe":recipe}
    )
def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        recipe.title = request.POST.get("title")
        recipe.servings = request.POST.get("servings")
        recipe.memo = request.POST.get("memo")
        recipe.reference_url = request.POST.get("reference_url")
        recipe.ingredients = request.POST.get("ingredients")
        recipe.save()
        
        return redirect("recipe_detail", recipe_id=recipe.id)
    
    return render(
        request,
        "app/recipe_edit.html",
        {"recipe":recipe}   
    )
def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return redirect("home")
    
def shoppinng_list(request):
    return render(request,"app/shopping_list.html")

def calendar_view(request):
    return render(request, "app/calendar.html")

def mypage(request):
    return render(request, "app/mypage.html")

def calendar_add(request):
    return render(request,"app/calendar_add.html")

def recipe_create(request):
    if request.method == "POST":
       title = request.POST.get("title")
       servings = request.POST.get("servings")
       memo = request.POST.get("memo")
       reference_url = request.POST.get("reference_url")
       ingredient_name = request.POST.get("ingredient_name")
       ingredient_amount = request.POST.get("ingredient_amount")
       
       ingredients = f"{ingredient_name} {ingredient_amount}"
       
       Recipe.objects.create(
            title=title,
            servings=servings,
            memo=memo,
            reference_url=reference_url,
            ingredients=ingredients
       )
       return redirect("home")    
    return render(request,"app/recipe_create.html")

def mypage_edit(request):
    return render(request,"app/mypage_edit.html")