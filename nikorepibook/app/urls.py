from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("recipe/",
         views.recipe_detail,
         name="recipe_detail"),
    path("shopping_list/",views.shoppinng_list,
         name="shopping_list"),
    path("calendar/",views.calendar_view,
         name="calendar"),
    path("mypage/",views.mypage,name="mypage"),
    path("calendar_add/",views.calendar_add,
         name="calendar_add"),
    
    
    

]
