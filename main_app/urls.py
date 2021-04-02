from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),# path in quotes and method name after views (in this case method = index)
    path('login_page', views.login_page),
    path('dashboard', views.dashboard),
    path('kitchen', views.kitchen),
    path('find_dinner', views.find_dinner),
    path('make_dinner', views.make_dinner),
    path('make_dinner/recipe/<int:num>', views.make_dinner_num),
    path('user/register', views.user_create),
    path('login', views.login),



    path('logout', views.logout),

]

