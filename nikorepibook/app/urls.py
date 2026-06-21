from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("recipe/<int:recipe_id>/",
         views.recipe_detail,
         name="recipe_detail"),
    path("recipe/<int:recipe_id>/edit/",
     views.recipe_edit,
     name="recipe_edit"),
    path(
         "recipe/<int:recipe_id>/delete/",
         views.recipe_delete,
         name="recipe_delete"
    ),
    path("shopping_list/",views.shopping_list,
         name="shopping_list"),
    path("calendar/",views.calendar_view,
         name="calendar"),
    path("mypage/",views.mypage,name="mypage"),
    path("calendar_add/",views.calendar_add,
         name="calendar_add"),
    path("recipe_create/",
         views.recipe_create,name="recipe_create"),
    path("mypage_edit/",
         views.mypage_edit,name="mypage_edit"),
    path(
         "shopping-item/<int:item_id>/toggle/",
         views.toggle_shopping_item,
         name="toggle_shopping_item"
    ),
    
    path("logout/", views.logout_view, name="logout"),
    
    
    

]
