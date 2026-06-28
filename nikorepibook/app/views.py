from django.shortcuts import render,redirect
from .models import Recipe,Ingredient,UserProfile,ShoppingItem,Menu,RecipeImage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
import calendar
from datetime import date
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def home(request):
    keyword = request.GET.get("keyword", "")
    ingredient = request.GET.get("ingredient", "")
    
    
    recipes = Recipe.objects.filter(
        user=request.user
    )
    
    if keyword:
        ingredient_recipe_ids = Ingredient.objects.filter(
            name__icontains=keyword,
            recipe__user=request.user
        ).values_list("recipe_id", flat=True)
        
        recipes = recipes.filter(
            Q(title__icontains=keyword) |
            Q(id__in=ingredient_recipe_ids)
        ).distinct()
        
    if ingredient:
        recipe_ids = Ingredient.objects.filter(
            name__icontains=ingredient,
            recipe__user=request.user
        ).values_list("recipe_id", flat=True)
        
        recipes = recipes.filter(id__in=recipe_ids)
        
    ingredient_tags = Ingredient.objects.filter(
        recipe__user=request.user
    ).exclude(
        name=""
    ).values_list(
        "name",
        flat=True
    ).distinct()
        
    return render(request,"app/home.html",{
        "recipes":recipes,
        "keyword": keyword,
        "ingredient": ingredient,
        "ingredient_tags": ingredient_tags,
        })

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        login(request, user)
        return redirect("home")
    return render(request,"app/signup.html")

def login_view(request):
    if request.method == "POST":
      email = request.POST.get("email")
      password = request.POST.get("password")
      
      user_obj = User.objects.filter(email=email).first()
      
      if user_obj is not None:
          user = authenticate(
             request,
             username=user_obj.username,
             password=password
          )
          
      
          if user is not None:
            login(request, user)
            return redirect("home")
      
    return render(request, "app/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def recipe_detail(request,recipe_id):
    recipe = Recipe.objects.get(
        id=recipe_id,
        user=request.user
    )
    ingredients = Ingredient.objects.filter(recipe=recipe)
    
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
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
    
@login_required    
def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(
        id=recipe_id,
        user=request.user
    )
    ingredients = Ingredient.objects.filter(recipe=recipe)
    
    if request.method == "POST":
        image = request.FILES.get("image")
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
            
            name = name.strip()
            unit = unit.strip()
            
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
            name = name.strip()
            unit = unit.strip()
            
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
            

        
        if image:
              recipe.image = image
              
        if request.POST.get("delete_main_image"):
            recipe.image.delete(save=False)
            recipe.image = None
        
        recipe.save()
        
        delete_sub_image_ids = request.POST.getlist("delete_sub_image_ids")
        
        delete_images = RecipeImage.objects.filter(
            id__in=delete_sub_image_ids,
            recipe=recipe
        )
        
        for delete_image in delete_images:
            delete_image.image.delete(save=False)
            delete_image.delete()
            
        
        images = request.FILES.getlist("images")
        
        for image_file in images:
            RecipeImage.objects.create(
                recipe=recipe,
                image=image_file
            )

        return redirect("recipe_detail", recipe_id=recipe.id)
    
    return render(
        request,
        "app/recipe_edit.html",
        {
            "recipe":recipe,
            "ingredients":ingredients,
            }   
    )
    
@login_required
def recipe_delete(request, recipe_id):
    
    recipe = Recipe.objects.get(
        id=recipe_id,
        user=request.user
    )
    recipe.delete()
    return redirect("home")

@login_required    
def shopping_list(request):
    
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    if start_date and end_date:
        request.session["shopping_start_date"] = start_date
        request.session["shopping_end_date"] = end_date
    else:
        start_date = request.session.get(
            "shopping_start_date",
            date.today().strftime("%Y-%m-%d")
        )
        end_date = request.session.get(
            "shopping_end_date",
            date.today().strftime("%Y-%m-%d")
        )
    
    menus = Menu.objects.filter(
        user=request.user,
        planned_date__range=[
            start_date,
            end_date
        ]
    )
    
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    user_servings = profile.adult_count + profile.child_count * Decimal(0.5)
    
    shopping_items = {}
    
    for menu in menus:
        ingredients = Ingredient.objects.filter(recipe=menu.recipe)
        
        for ingredient in ingredients:
            key = ingredient.name + ingredient.unit
            
            converted_quantity = (
                ingredient.base_quantity
                * user_servings
                / Decimal(menu.recipe.servings)
            )
            
            if ingredient.is_integer_only:
                converted_quantity = int(converted_quantity)
            
            if key not in shopping_items:
                shopping_items[key] = {
                    "name": ingredient.name,
                    "quantity": converted_quantity,
                    "unit": ingredient.unit,
                }
            else:
                shopping_items[key]["quantity"] += converted_quantity
            
    ShoppingItem.objects.filter(user=request.user).delete()
    
    for item in shopping_items.values():
        ShoppingItem.objects.update_or_create(
            user=request.user,
            name=item["name"],
            unit=item["unit"],
            defaults={
                "total_quantity": item["quantity"],
                    }
         )
    saved_items = ShoppingItem.objects.filter(user=request.user)
    
    for item in saved_items:
        if item.total_quantity == int(item.total_quantity):
            item.display_quantity = int(item.total_quantity)
        else:
            item.display_quantity = item.total_quantity
    
    
    return render(
        request,
        "app/shopping_list.html",
        {
         "shopping_items": saved_items,
         "start_date": start_date,
         "end_date": end_date,
         "menus": menus,
        }
    )
    
@login_required
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
        user=request.user,
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
    
@login_required   
def calendar_add(request):
    planned_date = request.GET.get("date")
    
    if not planned_date:
        planned_date = date.today().strftime("%Y-%m-%d")

    keyword = request.GET.get("keyword", "")
    selected_recipe_id = request.GET.get("recipe_id")
    
    
    recipes = Recipe.objects.filter(
        user=request.user
    )
    if keyword:
        recipes = recipes.filter(
            title__icontains=keyword
        )
    
    selected_menus = Menu.objects.filter(
        user=request.user,
        planned_date=planned_date
    )
    
    selected_recipe_ids = selected_menus.values_list(
        "recipe_id",
        flat=True
    )
    
    if request.method == "POST":
        recipe_ids = request.POST.getlist("recipe_ids")
        planned_date = request.POST.get("planned_date")
        
        
        if not planned_date:
            planned_date = date.today().strftime("%Y-%m-%d")
        
        Menu.objects.filter(
            user=request.user,
            planned_date=planned_date
        ).delete()
        
        for recipe_id in recipe_ids:
            recipe = Recipe.objects.get(
                id=recipe_id,
                user=request.user
            )
            
            Menu.objects.create(
                user=request.user,
                recipe=recipe,
                planned_date=planned_date
            )
            
        return redirect("calendar")
    
    return render(
        request,
        "app/calendar_add.html",
        {
            "recipes":recipes,
            "planned_date": planned_date,
            "selected_recipe_ids": selected_recipe_ids,
            "keyword": keyword,
            "selected_recipe_id": selected_recipe_id,
        }
    )

@login_required
def recipe_create(request):
    if request.method == "POST":
       title = request.POST.get("title")
       servings = request.POST.get("servings")
       memo = request.POST.get("memo")
       reference_url = request.POST.get("reference_url")
       image = request.FILES.get("image")
       ingredient_names = request.POST.getlist("ingredient_name")
       ingredient_amounts = request.POST.getlist("ingredient_amount")
       ingredient_units = request.POST.getlist("ingredient_unit")
       integer_only_list = request.POST.getlist("is_integer_only")
       
       
       recipe = Recipe.objects.create(
            user=request.user,
            title=title,
            servings=servings,
            memo=memo,
            reference_url=reference_url,
            image=image,
       )
       
       images = request.FILES.getlist("images")
       
       
       for image_file in images:
            RecipeImage.objects.create(
                recipe=recipe,
                image=image_file
            ) 
       
       for index,(name, amount,unit) in enumerate ( 
            zip(
                ingredient_names,
                ingredient_amounts,
                ingredient_units
            )
        ):
            
            name = name.strip()
            unit = unit.strip()
            
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


@login_required
def mypage(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    return render(request, "app/mypage.html",{
        "profile":profile
    })

@login_required
def mypage_edit(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    if request.method == "POST":
        image = request.FILES.get("image")
        profile.adult_count = request.POST.get("adult_count")
        profile.child_count = request.POST.get("child_count")
        
        if image:
            profile.image = image
            
        profile.save()
        
        return redirect("mypage")
        
    return render(request,"app/mypage_edit.html",{
        "profile": profile
    })

@login_required    
def toggle_shopping_item(request, item_id):
    item = ShoppingItem.objects.get(id=item_id)
    
    item.is_checked = not item.is_checked
    item.save()
    
    return JsonResponse({
        "success": True,
        "is_checked": item.is_checked
    })