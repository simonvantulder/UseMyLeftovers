from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),# path in quotes and method name after views (in this case method = index)
    path('login_page', views.login_page),
    path('home', views.home),
    # path('dashboard', views.dashboard),
    path('kitchen', views.kitchen),
    path('find_dinner', views.find_dinner),
    path('meal_wizard', views.meal_wizard),
    path('make_dinner/<int:num>', views.meal_wizard_leftovers),
    path('make_dinner/results', views.make_dinner_results),
    # path('make_dinner/recipe/<int:num>', views.make_dinner_num),
    path('user/register', views.user_create),
    path('login', views.login),
    path('view_all/<int:num>', views.view_all),
    path('ingredient_add', views.ingredient_add),
    path('ingredient_add/<int:num>', views.ingredient_add_in_category),
    path('ingredient_create', views.ingredient_create),
    path('recipe/<int:num>', views.recipe),
    path('delete/<int:num>', views.delete),
    path('logout', views.logout),

]

