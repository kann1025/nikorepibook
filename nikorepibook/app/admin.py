from django.contrib import admin
from .models import Recipe,Ingredient
from .models import UserProfile

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(UserProfile)

