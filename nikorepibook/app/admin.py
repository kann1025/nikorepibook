from django.contrib import admin
from .models import Recipe,Ingredient
from .models import UserProfile

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "amount",
        "base_quantity",
        "is_integer_only",
    )



admin.site.register(Recipe)
admin.site.register(UserProfile)

