from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    servings = models.IntegerField(default=2)
    reference_url = models.URLField(blank=True)
    memo = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    unit = models.CharField(max_length=20,blank=True)
    base_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    is_integer_only = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    adult_count = models.IntegerField(default=1)
    child_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    
class ShoppingItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    total_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    unit = models.CharField(max_length=20, blank=True)
    is_checked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return self.name 
   
   
class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    planned_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.planned_date} - {self.recipe.title}"