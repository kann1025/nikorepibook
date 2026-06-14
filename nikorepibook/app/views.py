from django.shortcuts import render,redirect
from .models import Recipe,Ingredient,UserProfile,ShoppingItem,Menu
from decimal import Decimal
import calendar
from datetime import date

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
    menus = Menu.objects.all()
    
    shopping_items = {}
    
    for menu in menus:
        ingredients = Ingredient.objects.filter(recipe=menu.recipe)
        
        for ingredient in ingredients:
            key = ingredient.name + ingredient.unit
            
            if key not in shopping_items:
                shopping_items[key] = {
                    "name": ingredient.name,
                    "quantity": ingredient.base_quantity,
                    "unit": ingredient.unit,
                }
            else:
                shopping_items[key]["quantity"] += ingredient.base_quantity
    
    return render(
        request,
        "app/shopping_list.html",
        {
         "shopping_items": shopping_items.values()
        }
    )

def calendar_view(request):
    today = date.today()
    
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1
        
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
        
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdatescalendar(year,month)
    
    menus  = Menu.objects.filter(
        planned_date__year=year,
        planned_date__month=month
    )
    
    calendar_weeks = []
    
    for week in weeks:
        week_data = []
        
        for day in week:
            day_menus = menus.filter(planned_date=day)
            
            week_data.append({
                "date": day,
                "day": day.day,
                "is_current_month": day.month == month,
                "is_today": day == today,
                "menus": day_menus,
            })
        calendar_weeks.append(week_data)
        
    return render(
        request,
        "app/calendar.html",
        {
            "calendar_weeks": calendar_weeks,
            "year": year,
            "month": month,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "next_year": next_year,
            "next_month": next_month,
        }
    )
    
    
def calendar_add(request):
    recipes = Recipe.objects.all()
    planned_date = request.GET.get("date","2026-03-10")
    
    if request.method == "POST":
        recipe_ids = request.POST.getlist("recipe_ids")
        planned_date = request.POST.get("planned_date")
        
        for recipe_id in recipe_ids:
            recipe = Recipe.objects.get(id=recipe_id)
            
            Menu.objects.create(
                user_id=1,
                recipe=recipe,
                planned_date=planned_date
            )
            
        return redirect("calendar")
    
    return render(
        request,
        "app/calendar_add.html",
        {
            "recipes":recipes,
            "planned_date": planned_date
        }
    )

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