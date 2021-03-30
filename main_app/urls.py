from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),# path in quotes and method name after views (in this case method = index)
    path('/login', views.login_page),
    path('user/register', views.user_create),
    path('login', views.login),


    path('logout', views.logout),

]

