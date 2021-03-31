from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
from . API import *

def index(request):
    return redirect ("/login_page")


def login_page(request):
    return render (request, "login_page.html")


def dashboard(request):
    # findByIngredients()
    # findByIngredientsTasty(request.POST)
    # print(findByIngredientsTasty())
    # findRecipe()
    # FindTags()
    
    return render (request, "dashboard.html")


def find_dinner(request):
    request.session["ideas"] = findByIngredientsTasty(request.POST)
    # print(request.session["ideas"][1])
    print(findByIngredientsTasty(request.POST))
    # print(find_by_ingredients(request.POST))
    # print("test")

    return redirect ("/make_dinner")


def make_dinner(request):
    idea = request.session['ideas']
    # print(idea)
    print(idea['results'])
    context = {
        "ideas" : idea['results'][0]['sections'][0]['components'],
        "idea" : idea['results'][0]
    
    }
    return render (request, "dashboard.html", context)


def user_create(request):
    errors = User.objects.validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = hash_browns,
            )
        request.session['uuid'] = user.id

    return redirect ("/dashboard")


def login(request):
    errors = User.objects.login_validator(request.POST)
    # API.findByIngredients()

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user_list = User.objects.filter(email = request.POST['email'])
        user = user_list[0]
        request.session['uuid'] = user.id 

        return redirect("/dashboard")



def logout(request):
    del request.session['uuid']
    
    return redirect("/")

