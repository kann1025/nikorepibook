from django.shortcuts import render,redirect
from .models import Recipe,Ingredient,UserProfile
from decimal import Decimal

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
    ingredients = Ingredient.objects.filter(recipe=recipe)
    
    profile = UserProfile.objects.get(user=request.user)
    
    family_servings = (
        Decimal(profile.adult_count)
        + (Decimal(profile.child_count) * Decimal("0.5"))
        )
    
    for ingredient in ingredients:
        calculated_quantity = (
            ingredient.base_quantity
            * family_servings
            / recipe.servings
        )
        
        if ingredient.is_integer_only:
            calculated_quantity = int(calculated_quantity)
            
        ingredient.calculated_quantity = calculated_quantity
        
        if calculated_quantity == int(calculated_quantity):
            ingredient.calculated_quantity = int(calculated_quantity)
        else:
            ingredient.calculated_quantity = calculated_quantity


    
    return render(
        request,
        "app/recipe_detail.html",
        {
            "recipe":recipe,
            "ingredients":ingredients,
            "family_servings": family_servings,
    })
    
    
def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = Ingredient.objects.filter(recipe=recipe)
    
    if request.method == "POST":
        recipe.title = request.POST.get("title")
        recipe.servings = request.POST.get("servings")
        recipe.memo = request.POST.get("memo")
        
        recipe.reference_url = request.POST.get("reference_url")
        
        ingredient_ids = request.POST.getlist("ingredient_id")
        ingredient_names = request.POST.getlist("ingredient_name")
        ingredient_amounts = request.POST.getlist("ingredient_amount")
        ingredient_units = request.POST.getlist("ingredient_unit")
        integer_only_ids = request.POST.getlist("is_integer_only")
        
        delete_ingredient_ids = request.POST.getlist("delete_ingredient_id")
        
        new_ingredient_names = request.POST.getlist("new_ingredient_name")
        new_ingredient_amounts = request.POST.getlist("new_ingredient_amount")
        new_ingredient_units = request.POST.getlist("new_ingredient_unit")
        new_integer_only_list = request.POST.getlist("new_is_integer_only")
        
        for ingredient_id, name, amount,unit in zip(
            ingredient_ids,
            ingredient_names,
            ingredient_amounts,
            ingredient_units,
        ):
            ingredient = Ingredient.objects.get(id=ingredient_id)
            
            if ingredient_id in delete_ingredient_ids:
                ingredient.delete()
            else:
                ingredient.name = name
                ingredient.amount = amount
                ingredient.base_quantity = amount
                ingredient.unit = unit
                ingredient.is_integer_only = ingredient_id in integer_only_ids
                
                ingredient.save()
  
            
        for index, (name, amount,unit) in enumerate ( zip(
            new_ingredient_names, 
            new_ingredient_amounts,
            new_ingredient_units 
        )):
            if name != "" or amount != "":
                Ingredient.objects.create(
                    recipe=recipe,
                    name=name,
                    amount=amount,
                    base_quantity=amount,
                    unit=unit,
                    is_integer_only=(
                        str(index)
                        in new_integer_only_list
                    )
                )
            

        recipe.save()

        return redirect("recipe_detail", recipe_id=recipe.id)
    
    return render(
        request,
        "app/recipe_edit.html",
        {
            "recipe":recipe,
            "ingredients":ingredients,
            }   
    )
def recipe_delete(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return redirect("home")
    
def shoppinng_list(request):
    return render(request,"app/shopping_list.html")

def calendar_view(request):
    return render(request, "app/calendar.html")


def calendar_add(request):
    return render(request,"app/calendar_add.html")

def recipe_create(request):
    if request.method == "POST":
       title = request.POST.get("title")
       servings = request.POST.get("servings")
       memo = request.POST.get("memo")
       reference_url = request.POST.get("reference_url")
       ingredient_names = request.POST.getlist("ingredient_name")
       ingredient_amounts = request.POST.getlist("ingredient_amount")
       ingredient_units = request.POST.getlist("ingredient_unit")
       integer_only_list = request.POST.getlist("is_integer_only")
       
       
       recipe = Recipe.objects.create(
            title=title,
            servings=servings,
            memo=memo,
            reference_url=reference_url,
       )  
       
       for index,(name, amount,unit) in enumerate ( 
            zip(ingredient_names, ingredient_amounts,ingredient_units)):
            if name and amount:
                 Ingredient.objects.create(
                    recipe=recipe,
                    name=name,
                    amount=amount,
                    unit=unit,
                    base_quantity=amount,
                    is_integer_only=str(index) in integer_only_list,
                 )
       
       return redirect("home")    
    return render(request,"app/recipe_create.html")

def mypage(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    return render(request, "app/mypage.html",{
        "profile":profile
    })


def mypage_edit(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    if request.method == "POST":
        profile.adult_count = request.POST.get("adult_count")
        profile.child_count = request.POST.get("child_count")
        profile.save()
        
        return redirect("mypage")
        
    return render(request,"app/mypage_edit.html",{
        "profile": profile
    })