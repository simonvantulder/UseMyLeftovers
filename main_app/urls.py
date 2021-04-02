from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),# path in quotes and method name after views (in this case method = index)
    path('login_page', views.login_page),
    path('home', views.home),
    path('dashboard', views.dashboard),
    path('kitchen', views.kitchen),
    path('find_dinner', views.find_dinner),
    path('make_dinner', views.make_dinner),
    path('make_dinner/recipe/<int:num>', views.make_dinner_num),
    path('user/register', views.user_create),
    path('login', views.login),
    path('view_all/<int:num>', views.view_all),
    path('add_ingredient', views.add_ingredient_page),
    path('ingredient_add', views.ingredient_add),


    path('logout', views.logout),

]

