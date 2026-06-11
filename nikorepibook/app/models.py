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
    base_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
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